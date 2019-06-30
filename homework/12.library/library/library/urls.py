"""library URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from django.urls import path, re_path
from app import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', views.login),
    path('register/', views.register),
    path('index/', views.index),
    path('logout/', views.logout),
    path('add_author/', views.add_author),
    re_path(r'edit_author/([0-9]*)/', views.edit_author),
    re_path(r'show_author/([0-9]*)/', views.show_author),
    re_path(r'del_author/([0-9]*)/', views.del_author),
    path('add_publish/', views.add_publish),
    re_path(r'edit_publish/([0-9]*)/', views.edit_publish),
    re_path(r'show_publish/([0-9]*)/', views.show_publish),
    re_path(r'del_publish/([0-9]*)/', views.del_publish),
]
