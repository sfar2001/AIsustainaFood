from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('accounts/', include('django.contrib.auth.urls')),
    path('accounts/', include('accounts.urls')),
    path('stock/', include('stockmgmt.urls')),
    path('', include('stockmgmt.urls')),  # This makes the dashboard the home page
]