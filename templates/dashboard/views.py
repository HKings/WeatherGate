from django.shortcuts import render
from django.contrib.auth.decorators import login_required

@login_required
def dashboard_view(request):
    # Main dashboard view - requires authentication
    return render(request, 'dashboard/dashboard.html')

