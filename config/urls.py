"""
URL configuration for config project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
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
from core import views

urlpatterns = [
    path('', views.home, name="home"),
    path('services/', views.services, name="services"),
    path('about/', views.about, name="about"),
    path('contact/', views.contact, name="contact"),
    path('products/', views.products, name="products"),
    path('cart/', views.cart, name="cart"),
    path('admin/', admin.site.urls),
    path('add-to-cart/<int:product_id>/', views.add_to_cart, name="add_to_cart"),
    path('cart/increase/<int:product_id>/', views.increase_cart, name="increase_cart"),
    path('cart/decrease/<int:product_id>/', views.decrease_cart, name="decrease_cart"),
    path('cart/remove/<int:product_id>/', views.remove_from_cart, name="remove_from_cart"),
    path('checkout/', views.checkout, name="checkout"),
    path('payment/<int:order_id>/', views.payment, name='payment'),
    path('payment-callback/', views.payment_callback, name='payment_callback'),
]
