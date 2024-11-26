from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, authenticate, get_user_model, logout
from .forms import SignUpForm, CustomAuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.core.mail import send_mail
from django.shortcuts import render
from django.contrib import messages
from django.http import JsonResponse
from .models import Cart, CartItem, Product
from django.contrib.auth.decorators import login_required
# Create your views here.
def cust_about(request): 
  return render(request, 'about.html')

def cust_home(request): 
  return render(request, 'dashboard_customer/homepage.html')

def cust_agentform(request): 
  return render(request, 'dashboard_customer/agent.html')

def cust_contact(request):
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
    
    return render(request, 'dashboard_customer/contact.html')

def cust_order(request): 
  return render(request, 'dashboard_customer/order.html')

def cust_pay(request): 
  return render(request, 'dashboard_customer/pay.html')

def cust_profile(request):
    return render(request, 'dashboard_customer/profile.html')

def cust_listpay(request):
    return render(request, 'dashboard_customer/listpay.html')
#================== agent =======================
def agent_home(request): 
  return render(request, 'dashboard_agent/homepage.html')

def agent_about(request): 
  return render(request, 'dashboard_agent/about.html')

def agent_contact(request):
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
    
    return render(request, 'dashboard_agent/contact.html')

# def agent_detail(request): 
#   return render(request, 'dashboard_agent/detail.html')

def agent_order(request): 
  return render(request, 'dashboard_agent/order.html')

def agent_pay(request): 
  return render(request, 'dashboard_agent/pay.html')

def agent_profile(request):
    return render(request, 'dashboard_agent/profile.html')

def agent_listpay(request):
    return render(request, 'dashboard_agent/listpay.html')

@login_required
def cart_summary_agent(request):
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
    return render(request, 'shopping/cart_summary_agent.html', context)
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
                return redirect('/admin/')  # arahkan ke admin paner
            elif user.groups.filter(name='AGENT'):
                return redirect('agent_home')  # dashboard agent
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
	messages.success(request, ("You have been logged out...Thanks for stopping by..."))
	return redirect('home')

def signup_view(request):
    if request.method == 'POST':
        form = SignUpForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect(cust_home)  
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

def product_detail(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Ambil produk berdasarkan slug
    return render(request, 'dashboard_customer/detail.html', {'product': product})

def product_detail_agent(request, slug):
    product = get_object_or_404(Product, slug=slug)  # Ambil produk berdasarkan slug
    return render(request, 'dashboard_agent/detail.html', {'product': product})
  
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
        quantity = int(request.POST.get("quantity", 1))  # Default quantity = 1

        # Ambil produk berdasarkan ID
        product = get_object_or_404(Product, id=product_id)

        # Cek stok produk
        if product.stock < quantity:
            return JsonResponse({"status": "error", "message": "Insufficient stock!"}, status=400)

        # Ambil atau buat keranjang untuk user
        cart, created = Cart.objects.get_or_create(user=request.user)

        # Periksa apakah produk sudah ada di keranjang
        cart_item, created = CartItem.objects.get_or_create(cart=cart, product=product)

        if not created:
            cart_item.quantity += quantity  # Tambahkan quantity jika sudah ada
        else:
            cart_item.quantity = quantity  # Set quantity jika baru ditambahkan

        cart_item.save()

        # Kurangi stok produk
        product.stock -= quantity
        product.save()

        return JsonResponse({"status": "success", "message": "Product added to cart!"})
        

    return JsonResponse({"status": "error", "message": "Invalid request!"}, status=400)

