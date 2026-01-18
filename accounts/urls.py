from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

urlpatterns = [
    # Using Django's built-in LoginView
    path('login/', auth_views.LoginView.as_view(template_name='accounts/login.html'), name='login'),
    
    # Using our custom logout and register views
    path('logout/', views.logout_view, name='logout'),
    path('register/', views.register_view, name='register'),
]