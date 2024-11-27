from django.urls import path
from . import views

urlpatterns = [
    path('', views.cust_home, name='home'),
    # path('customer_home', views.cust_home, name='cust_home'),
    path('productlist/', views.cust_productlist, name='cust_productlist'),
    path('become agent/', views.cust_agentform, name='cust_agentform'),
    path('agent_product/', views.agent_productlist, name='agent_productlist'),
    path('agent_home/', views.agent_home, name='agent_home'), #hilangkan
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.cust_contact, name='contact'),
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('order/', views.cust_order, name='cust_order'),
    path('pay/', views.cust_pay, name='cust_pay'),
    path('agent_contact/', views.agent_contact, name='agent_contact'),
    # path('agent_detail', views.agent_detail, name='agent_detail'),
    path('agent_order/', views.agent_order, name='agent_order'),
    path('agent_pay/', views.agent_pay, name='agent_pay'),
    # ================ cart ======================
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
]