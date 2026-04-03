from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # Accounts app URLs (register, login, MFA, logout)
    path('accounts/', include('accounts.urls')),

    # Dashboard app URLs
    path('dashboard/', include('dashboard.urls')),
]

