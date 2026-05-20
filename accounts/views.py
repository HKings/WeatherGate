from django.shortcuts import render, redirect
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.core.mail import send_mail
from django.conf import settings
from .models import CustomUser
from django.template.loader import render_to_string
from django.contrib.auth.decorators import login_required


def register_view(request):
    """
    Handles new user registration.
    Creates the account as inactive, sends confirmation token by email.
    Account is only activated after email confirmation.
    """
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')

        # Check if email already exists in the database
        if CustomUser.objects.filter(email=email).exists():
            messages.error(request, 'Email already registered.')
            return redirect('register')

        # Check if username already exists in the database
        if CustomUser.objects.filter(username=username).exists():
            messages.error(request, 'Username already taken.')
            return redirect('register')

        # Create the user as inactive until email is confirmed
        user = CustomUser.objects.create_user(
            username=username,
            email=email,
            password=password,
            is_active=False
        )

        # Generate confirmation token and save
        token = user.generate_mfa_token()
        user.save()

        # Store user ID in session for confirmation step
        request.session['register_user_id'] = user.id

        # Send confirmation email
        html_message = render_to_string('emails/email_verify.html', {'token': token})
        send_mail(
            subject='WeatherGate — Confirm your email',
            message=f'Your confirmation code is: {token}',
            from_email=settings.EMAIL_HOST_USER,
            recipient_list=[email],
            html_message=html_message,
        )

        return redirect('email_verify')

    return render(request, 'accounts/register.html')


def email_verify_view(request):
    """
    Handles email confirmation after registration.
    Validates the token and activates the account.
    On success, redirects to login with success message.
    """
    if request.method == 'POST':
        token = request.POST.get('token')
        user_id = request.session.get('register_user_id')

        if not user_id:
            return redirect('register')

        try:
            user = CustomUser.objects.get(id=user_id)

            if not user.is_mfa_token_valid():
                messages.error(request, 'Verification code has expired. Please login again.')
                return redirect('login')

            if user.mfa_token == token:
                # Token valid — activate account and mark email as verified
                user.is_active = True
                user.is_email_verified = True
                user.mfa_token = None
                user.save()

                # Clear session
                del request.session['register_user_id']

                messages.success(request, 'Account created successfully. Please login!')
                return redirect('login')
            else:
                messages.error(request, 'Invalid confirmation code.')
                return redirect('email_verify')

        except CustomUser.DoesNotExist:
            return redirect('register')

    return render(request, 'accounts/mfa_verify.html')
    
def login_view(request):
    """
    Handles user login — first step of the MFA flow.
    Validates email and password, then generates a 6-digit token
    and sends it to the user's email before redirecting to MFA verification.
    """
    if request.method == 'POST':
        email = request.POST.get('email')
        password = request.POST.get('password')

        try:
            user = CustomUser.objects.get(email=email) # Find the user by email (Django uses username internally)
            user = authenticate(request, username=user.username, password=password) # Authenticate using Django's built-in system

            if user is not None:
                # Generate a new 6-digit MFA token and save it to the database
                token = user.generate_mfa_token()
                user.save()

                # Temporarily store the user ID in the session for the MFA step
                request.session['mfa_user_id'] = user.id 

                # Send the token to the user's email
                html_message = render_to_string('emails/mfa_email.html', {'token': token})
                send_mail(
                    subject='WeatherGate - Your verification code',
                    message=f'Your verification code is: {token}',
                    from_email=settings.EMAIL_HOST_USER,
                    recipient_list=[email],
                    html_message=html_message,
                )
                return redirect('mfa_verify')
            else:
                messages.error(request, 'Invalid email or password.')
                return redirect('login')
            
        except CustomUser.DoesNotExist:
            # User not found, return same error to avoid exposing valid emails
            messages.error(request, 'Invalid email or password!')
            return redirect('login')
    
    # If GET request, just render the login form
    return render(request, 'accounts/login.html')
    
def mfa_verify_view(request):
    """
    Handles MFA token verification — second step of the login flow.
    Retrieves the user ID stored in the session, validates the token,
    and logs the user in if correct. Redirects to dashboard on success.
    """
    if request.method == 'POST':
        token = request.POST.get('token')
        user_id= request.session.get('mfa_user_id') # Retrieve the user ID stored during the login step

        # If no user ID in session, force back to login
        if not user_id:
            return redirect('login')
        
        try:
            user = CustomUser.objects.get(id=user_id)

            if not user.is_mfa_token_valid():
                messages.error(request, 'Verification code has expired. Please login again.')
                return redirect('login')

            if user.mfa_token == token:
                # Token matches, mark MFA as verified and log the user in
                user.mfa_verified = True
                user.save()
                login(request, user, backend='django.contrib.auth.backends.ModelBackend')
                return redirect('dashboard')
            else:
                # Token does not match, show error and try again
                messages.error(request, 'Invalid verification code.')
                return redirect('mfa_verify')
            
        except CustomUser.DoesNotExist:
            return redirect('login')
    
    # If GET request, just render the MFA verification form
    return render(request, 'accounts/mfa_verify.html')
    
def logout_view(request):
    """
    Handles user logout.
    Clears the session and redirects to the login page.
    """
    logout(request)
    return redirect('login')

@login_required
def profile_view(request):
    """
    Handles user profile page.
    Allows the user to upload a profile avatar.
    """
    if request.method == 'POST' and request.FILES.get('avatar'):
        # Save the uploaded avatar
        request.user.avatar = request.FILES['avatar']
        request.user.save()
        messages.success(request, 'Profile photo updated successfully.')
        return redirect('profile')

    return render(request, 'accounts/profile.html')

