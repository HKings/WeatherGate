from django.urls import path
from . import views

urlpatterns = [
    # Main weather dashboard
    path('', views.dashboard_view, name='dashboard'),
]