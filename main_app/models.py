from django.db import models

# Create your models here.
from django.contrib.auth.models import AbstractUser, Group
from django.db import models
from django.utils.text import slugify
from django.core.validators import MinLengthValidator


class CustomUser(AbstractUser):
    USER_TYPE_CHOICES = (
        ('admin', 'Admin'),
        ('customer', 'Customer'),
        ('agent', 'Agent'),
    )
    profile_image = models.ImageField(upload_to='profile_pics/', null=True, blank=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='Customer')
    phone = models.CharField(max_length=15, blank=True)
    address = models.TextField(blank=True)

    # Untuk agen
    company_name = models.CharField(max_length=100, blank=True, null=True)
    company_address = models.CharField(max_length=250, blank=True, null=True)
    company_email = models.EmailField(max_length=100, blank=True)
    company_contact = models.CharField(max_length=15 , blank=True, null=True)
    npwp = models.CharField(max_length=16, validators=[MinLengthValidator(16, message="NPWP must be exactly 16 characters.")], blank=True, null=True)
    photo = models.ImageField(upload_to='company_picture/', null=True, blank=True)
    is_verified = models.BooleanField(default=False)

    def save(self, *args, **kwargs):
        # Pastikan pengguna masuk grup sesuai tipe user
        super().save(*args, **kwargs)
        group, created = Group.objects.get_or_create(name=self.user_type.upper())
        self.groups.add(group)


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = models.SlugField(unique=True)
    
    def __str__(self):
        return self.name
    
    class Meta:
        verbose_name_plural = 'Categories'

class Product(models.Model):
    USER_TYPE_CHOICES = (('agent', 'Agent'), ('customer', 'Customer'),)
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
    name = models.CharField(max_length=200)
    slug = models.SlugField(unique=True, blank=True, null=True)  # Tambahkan slug
    description = models.TextField()
    image = models.ImageField(upload_to='products/')
    price = models.DecimalField(max_digits=10, decimal_places=2)
    stock = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            base_slug = slugify(self.name)
            slug = base_slug
            count = 1
            while Product.objects.filter(slug=slug).exists():
                slug = f"{base_slug}-{count}"
                count += 1
            self.slug = slug
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name


class Cart(models.Model):
    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def get_total_price(self):
        # Menghitung total harga dari semua item di dalam keranjang
        total = sum(item.get_total() for item in self.cartitem_set.all())
        return total

    def __str__(self):
        return f"Cart of {self.user.username}"

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField(default=0)
    
    def get_total(self):
        return self.product.price * self.quantity

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"


class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('paid', 'Paid'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('completed', 'Completed'),
        ('cancelled', 'Cancelled'),
    )
    
    user = models.ForeignKey(CustomUser, on_delete=models.SET_NULL, null=True, blank= True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    contact = models.CharField(max_length=15, blank=True)
    payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=10, decimal_places=2)  # Harga saat pembelian

class AgentApplication(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected'),
    )

    user = models.OneToOneField(CustomUser, on_delete=models.CASCADE, related_name='agent_application')
    company_name = models.CharField(max_length=100)
    company_address = models.CharField(max_length=250, blank=True, null=True)
    company_email = models.EmailField(max_length=100, blank=True, null=True)
    company_contact = models.CharField(max_length=15, blank=True, null=True)
    npwp = models.CharField(max_length=16, validators=[MinLengthValidator(16, message="NPWP must be exactly 16 characters.")],)
    photo = models.ImageField(upload_to='company_picture/', blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Application by {self.user.username} - {self.status}"

from django.db.models.signals import post_save
from django.dispatch import receiver

#signal untuk mengupdate status dan type user setelah form agent diverifikasi
@receiver(post_save, sender=AgentApplication)
def approve_agent_application(sender, instance, **kwargs):
    if instance.status == 'approved':
        user = instance.user
        user.is_verified = True
        user.user_type = 'agent'
        user.company_name = instance.company_name
        user.company_address = instance.company_address
        user.save()

#signal untuk memasukkan user ke grup AGENT      
@receiver(post_save, sender=CustomUser)
def add_user_to_agent_group(sender, instance, **kwargs):
    if instance.user_type == 'AGENT':
        group, created = Group.objects.get_or_create(name='AGENT')
        if not instance.groups.filter(name='AGENT').exists():
            instance.groups.add(group)

# Signal untuk membuat Cart otomatis saat CustomUser dibuat
@receiver(post_save, sender=CustomUser)
def create_cart_for_new_user(sender, instance, created, **kwargs):
    if created:
        # Jika user baru dibuat, buatkan Cart baru yang terkait dengan user tersebut
        Cart.objects.get_or_create(user=instance)            