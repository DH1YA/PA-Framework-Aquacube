from django.urls import path
from . import views

urlpatterns = [
    path('', views.cust_home, name='home'),
    path('customer_home', views.cust_home, name='cust_home'),
    path('productlist', views.cust_productlist, name='cust_productlist'),
    path('become agent', views.cust_agentform, name='cust_agentform'),
    path('agent_product', views.agent_productlist, name='agent_productlist'),
    path('agent_home', views.agent_home, name='agent_home'),
    path('login', views.login_view, name='login'),
    path('signup', views.signup_view, name='signup'),
    
]