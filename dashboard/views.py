from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .services import get_weather

@login_required
def dashboard_view(request):
    """
    Main dashboard view requires authentication.
    Fetches weather data based on user search or defaults to Lisbon.
    """
    city = request.GET.get('city', 'Lisbon')
    weather = get_weather(city)

    context = {
        'weather': weather,
        'city': city,
    }

    return render(request, 'dashboard/dashboard.html', context)
