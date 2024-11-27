from django.db.models import Sum  
from .models import Cart  

def cart_item_count(request):
    if request.user.is_authenticated:
        try:
            cart = Cart.objects.get(user=request.user)
            # Menghitung total item berdasarkan jumlah (quantity)
            item_count = cart.cartitem_set.count()
        except Cart.DoesNotExist:
            item_count = 0
    else:
        item_count = 0

    return {'cart_item_count': item_count}
