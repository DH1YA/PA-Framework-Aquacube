from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', views.home, name='home'),
    path('productlist/', views.cust_productlist, name='cust_productlist'),
    path('become agent/', views.agent_form, name='agent_form'),
    path('agent_product/', views.agent_productlist, name='agent_productlist'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('signup/', views.signup_view, name='signup'),
    path('about/', views.about, name='about'),
    path('contact/', views.contact, name='contact'),
    path('product_detail/<slug:slug>/', views.product_detail, name='product_detail'),
    path('profile/', views.profile, name='profile'),
    path('listagent/', views.listagent, name='listagent'),
    # ================ cart and shop ======================
    path('payment/', views.payment, name='payment'),
    path('direct_order/<int:product_id>/', views.direct_order_page, name='direct_order'),
    path('process_order/', views.process_order, name='process_order'),
    path('add-to-cart/', views.add_to_cart, name='add_to_cart'),
    path('cart/', views.cart_summary, name='cart_summary'),
    path('cart/update/<int:item_id>/', views.update_cart_item, name='update_cart_item'),
    path('cart/remove/<int:item_id>/', views.remove_cart_item, name='remove_cart_item'),
    path('listpay/', views.listpay, name='listpay'),
    path('listorder/', views.listorder, name='listorder'),
    path('orders/', views.order_history, name='order_history'),
    path('orders/<int:order_id>/', views.order_detail, name='order_detail'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)