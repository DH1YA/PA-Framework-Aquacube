from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('productlist/', views.cust_productlist, name='cust_productlist'),
    path('become agent/', views.cust_agentform, name='cust_agentform'),
    path('agent_product/', views.agent_productlist, name='agent_productlist'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile, name='profile'),
    # ================ cart and shop ======================
    path('payment/', views.payment, name='payment'),
    path('direct_order/<int:product_id>/', views.direct_order_page, name='direct_order'),
    path('process_order/', views.process_order, name='process_order'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('listpay/', views.listpay, name='listpay'),
]