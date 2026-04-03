from django.urls import path
from . import views

urlpatterns = [
    # Registration page
    path('register/', views.register_view, name='register'),

    # Login page
    path('login/', views.login_view, name='login'),

    # MFA verification page
    path('mfa-verify/', views.mfa_verify_view, name='mfa_verify'),

    # Logout
    path('logout/', views.logout_view, name='logout'),
]