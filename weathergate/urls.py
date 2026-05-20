from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # Django admin panel
    path('admin/', admin.site.urls),

    # Accounts app URLs (register, login, MFA, logout)
    path('accounts/', include('accounts.urls')),

    # Dashboard app URLs
    path('dashboard/', include('dashboard.urls')),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

