"""
URL configuration for Aquacube project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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

urlpatterns = [
    path('admin/', admin.site.urls),
    path('home', views.customer_home),
    path('product', views.customer_product),
    path('agent', views.customer_agent),
    path('signin', views.customer_signin),
    path('signup', views.customer_signup),
    path('contact', views.customer_contact),
    path('about', views.customer_about),
    path('detail/product', views.customer_detail),
    path('order', views.customer_order),
    path('pay', views.customer_pay),

    path('home/agent', views.agent_home),
    path('product/agent', views.agent_product),
    path('contact/agent', views.agent_contact),
    path('about/agent', views.agent_about),
    path('detail/product/agent', views.agent_detail),
    path('order/agent', views.agent_order),
    path('pay/agent', views.agent_pay),
]
