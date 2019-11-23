"""YazilimBakimi URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.1/topics/http/urls/
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
from BankApp import views

urlpatterns = [
    path('admin/', admin.site.urls), 
    path('', views.index),
    path('login', views.logpage),
    path("signin",views.signin),
    path("signup",views.signup),
    path("logout",views.logoutpage),
    path("navbar",views.navbar),
    path("accounts", views.accounts),
    path("transfer", views.transfer),
    path("sendmoney", views.sendmoney),
    path("addaccount", views.addaccount),
    path("addmoney", views.addmoney),
    path("addmoneytobalance", views.addmoneytobalance),
    path("takemoney", views.takemoney),
    path("takemoneyfrombalance", views.takemoneyfrombalance),
    path("gettransactions", views.getaccounttransactions),
    path("deleteaccount", views.deleteaccount),
    path("profile", views.profile),
    path("updateprofile", views.profileupdate),
    path("deleteprofile", views.profiledelete),
    path("passwordupdate", views.updatepasswordpage),
    path("updatepassword", views.passwordupdate),
    path("gethgsproducts", views.gethgsproducts),
    path("buyhgsproducts", views.buyhgsproducts),
    path("get_user", views.get_user),
] 
