from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, logout
from .forms import SignUpForm, CustomAuthenticationForm, PaymentForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Product,Order, OrderItem
from django.contrib.auth.decorators import login_required
from django.db import transaction
# Create your views here.

def home(request): 
  return render(request, 'homepage.html')

def about(request): 
  return render(request, 'about.html')

def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        full_message = f"From: {name}\nEmail: {email}\n\n{message}"

        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=email, 
                recipient_list=['aquacubecompany@gmail.com'],  
            )
            messages.success(request, "Your message has been sent successfully!")
        except Exception as e:
            messages.error(request, "Failed to send your message. Please try again later.")
    
    return render(request, 'contact.html')

def profile(request):
    return render(request, 'profile.html')
# =============== Customer ========================

def cust_agentform(request): 
  return render(request, 'dashboard_customer/agent.html')

  
#================== agent =======================



#================= registration ===============
def login_view(request):
    User = get_user_model() #get_user_model untuk mengambil model autentikasi cutom pada setting.py
    if request.method == 'POST':
        form = CustomAuthenticationForm(data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            # Redirect user berdasarkan grup atau role
            if user.groups.filter(name='ADMIN'):
                return redirect('/admin/')  # arahkan ke admin panel
            else:
                return redirect('home')  # dashboard cutomer
        else:
            username = request.POST.get('username')
            password = request.POST.get('password')

            # Cek apakah username ada di database
            if not User.objects.filter(username=username).exists():
                messages.error(request, "Username tidak ditemukan.")
            else:
                # Jika username ada, berarti password salah
                user = authenticate(request, username=username, password=password)
                if user is None:
                    messages.error(request, "Password salah.")
            messages.error(request, 'Silahkan periksa kembali username atau password')
    else:
        form = CustomAuthenticationForm()
    return render(request, 'login.html', {'form': form})
  
def logout_view(request):
	logout(request)
	return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('home')  
    else:
        form = SignUpForm()
    return render(request, 'signup.html', {'form': form})

# ============== cart and product ===========================
def agent_productlist(request): 
  products = Product.objects.all()
  return render(request, 'dashboard_agent/product.html', {'products':products})

def cust_productlist(request): 
  products = Product.objects.filter(user_type='customer')
  return render(request, 'dashboard_customer/product.html', {'products':products})

@login_required 
def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Ambil produk berdasarkan slug
    return render(request, 'shopping/detail.html', {'product': product})
  
  
@login_required
def cart_summary(request):
    try:
        cart = Cart.objects.get(user=request.user)
        cart_items = cart.cartitem_set.all()
        total_price = cart.get_total_price()
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0

    context = {
        'cart_items': cart_items,
        'total_price': total_price,
    }
    return render(request, 'shopping/cart_summary.html', context)

@login_required
def update_cart_item(request, item_id):
    if request.method == 'POST':
        cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
        quantity = int(request.POST.get('quantity', 1))
        
        if quantity > 0 and quantity <= cart_item.product.stock:
            cart_item.quantity = quantity
            cart_item.save()
            messages.success(request, 'Cart updated successfully')
        else:
            messages.error(request, 'Invalid quantity')
    
    return redirect('cart_summary')

@login_required
def remove_cart_item(request, item_id):
    cart_item = get_object_or_404(CartItem, id=item_id, cart__user=request.user)
    cart_item.delete()
    messages.success(request, 'Item removed from cart')
    return redirect('cart_summary')

@login_required
def add_to_cart(request):
    if request.method == "POST":
        product_id = request.POST.get("product_id")
        quantity = int(request.POST.get("quantity", 1))

        product = get_object_or_404(Product, id=product_id)

        if quantity > product.stock or quantity <= 0:
            messages.error(request, "Invalid quantity.")
            return redirect("product_detail", product_id=product.id)

        cart, created = Cart.objects.get_or_create(user=request.user)
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        cart_item.quantity += quantity
        cart_item.save()

        messages.success(request, "Item added to cart.")
        return redirect("cart_summary")
    return redirect("cust_productlist")
  
@login_required
def direct_order_page(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    quantity = request.GET.get('quantity', 1)  # Ambil kuantitas dari query parameter

    try:
        quantity = int(quantity)
        if quantity < 1 or quantity > product.stock:
            raise ValueError("Invalid quantity")
    except ValueError:
        return redirect('product_detail', product_id=product_id)

    total_price = product.price * quantity

    context = {
        'product': product,
        'quantity': quantity,
        'total_price': total_price,
    }
    return render(request, 'shopping/order.html', context)

def process_order(request):
    if request.method == 'POST':
        product_id = request.POST.get('product_id')
        quantity = int(request.POST.get('quantity'))
        contact = request.POST.get('contact')
        payment_proof = request.FILES.get('payment_proof')

        product = get_object_or_404(Product, id=product_id)
        if quantity > product.stock:
            return redirect('direct_order_page', product_id=product_id)

        # Buat Order
        order = Order.objects.create(
            user=request.user,
            total_amount=product.price * quantity,
            contact=contact,
            payment_proof=payment_proof,
            status='pending'
        )

        # Buat OrderItem
        OrderItem.objects.create(
            order=order,
            product=product,
            quantity=quantity,
            price=product.price
        )

        # Kurangi stok produk
        product.stock -= quantity
        product.save()

        return redirect('home')  # Halaman sukses


  
@login_required
def payment(request):
    user = request.user  # Ambil user yang login
    try:
        # Pastikan keranjang diambil berdasarkan user
        cart = Cart.objects.get(user=user)
        cart_items = cart.cartitem_set.all()
        total_price = cart.get_total_price()
    except Cart.DoesNotExist:
        cart_items = []
        total_price = 0
        messages.warning(request, 'Your cart is empty. Please add items to proceed.')

    if request.method == 'POST':
        form = PaymentForm(request.POST, request.FILES)
        if form.is_valid():
            # Buat Order baru
            order = Order.objects.create(
                user=user,
                total_amount=total_price,
                payment_proof=form.cleaned_data['payment_proof'],
                contact=form.cleaned_data['contact']
            )

            # Pindahkan item dari Cart ke OrderItem
            for item in cart_items:
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )
                # Kurangi stok produk
                product = get_object_or_404(Product, id=item.product.id)
                product.stock -= item.quantity
                product.save()

            # Kosongkan Cart
            cart.cartitem_set.all().delete()

            messages.success(request, 'Payment successful! Order has been placed.')
            return redirect('home')

    else:
        form = PaymentForm()

    return render(request, 'shopping/payment.html', {
        'cart_items': cart_items,
        'total_price': total_price,
        'form': form
    })

def listpay(request):
    return render(request, 'shopping/listpay.html')