"""gesys URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from django.urls import path, include
from .views import Test, Login, Registro


urlpatterns = [
    # path('', Test.as_view(), name="list_products"),
    # path('delete/<int:pk>/', Test.as_view()),
    #path('update/<int:pk>/', Test.as_view()),
    #path('add/', Test.as_view()),
    path('login', Login.as_view(), name="login"), # corresponde a /api/login
    path('sign_up', Registro.as_view(), name="sign_up"), # corresponde a /api/login
]