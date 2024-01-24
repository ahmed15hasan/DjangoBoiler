"""
URL configuration for server project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from django.urls import include


 

urlpatterns = [
   
    path('admin/', admin.site.urls),
    # path('login', views.login),
    
    
    
    # path('signup', views.signup),
    # path('test_token/', views.test_token, name='test_token'),
    # path('profile/', views.view_profile, name='view_profile'),
    
    path('login/', views.login_view, name='login_view'),
    path('loginAction/', views.login_action, name='loginAction'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('logout/', views.logout_view, name='logout'), 
    path('profile/', views.profile_view, name='profile_view'),
    path('users/', views.user_view, name='users'),
   
    
    path('register/', views.register_view, name='register_view'),
    path('registerAction', views.register_action, name='register_action'),
]
