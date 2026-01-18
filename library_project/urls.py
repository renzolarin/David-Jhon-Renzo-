from django.contrib import admin
from django.urls import path, include

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.urls')), # This redirects the home page to your library app
    path('accounts/', include('accounts.urls')), # For login/registration
]