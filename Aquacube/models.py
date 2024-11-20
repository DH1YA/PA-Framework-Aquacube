# class Category(models.Model):
#     name = models.CharField(max_length=100)
#     slug = models.SlugField(unique=True)
    
#     def _str_(self):
#         return self.name
    
#     class Meta:
#         verbose_name_plural = 'Categories'

# class Product(models.Model):
#     USER_TYPE_CHOICES = ( ('agent', 'Agent'), ('customer', 'Customer'), )
#     category = models.ForeignKey(Category, on_delete=models.CASCADE)
#     user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, default='customer')
#     name = models.CharField(max_length=200)
#     slug = models.SlugField(unique=True)
#     description = models.TextField()
#     image = models.ImageField(upload_to='products/')
#     price = models.DecimalField(max_digits=10, decimal_places=2)
#     stock = models.IntegerField(default=0)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)
    
#     def _str_(self):
#         return self.name


# class Cart(models.Model):
#     user = models.OneToOneField(User, on_delete=models.CASCADE)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

#     def get_total_price(self):
#         # Menghitung total harga dari semua item di dalam keranjang
#         total = sum(item.get_total() for item in self.cartitem_set.all())
#         return total

#     def _str_(self):
#         return f"Cart of {self.user.username}"

# class CartItem(models.Model):
#     cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField(default=1)
    
#     def get_total(self):
#         return self.product.price * self.quantity

#     def _str_(self):
#         return f"{self.quantity} x {self.product.name}"


# class Order(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('paid', 'Paid'),
#         ('processing', 'Processing'),
#         ('shipped', 'Shipped'),
#         ('completed', 'Completed'),
#         ('cancelled', 'Cancelled'),
#     )
    
#     user = models.ForeignKey(User, on_delete=models.SET_NULL)
#     total_amount = models.DecimalField(max_digits=10, decimal_places=2)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     payment_proof = models.ImageField(upload_to='payment_proofs/', null=True, blank=True)
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)

# class OrderItem(models.Model):
#     order = models.ForeignKey(Order, on_delete=models.CASCADE)
#     product = models.ForeignKey(Product, on_delete=models.CASCADE)
#     quantity = models.IntegerField()
#     price = models.DecimalField(max_digits=10, decimal_places=2)  # Harga saat pembelian

# class AgentApplication(models.Model):
#     STATUS_CHOICES = (
#         ('pending', 'Pending'),
#         ('approved', 'Approved'),
#         ('rejected', 'Rejected'),
#     )
    
#     user = models.ForeignKey(User, on_delete=models.CASCADE)
#     company_name = models.CharField(max_length=100)
#     business_license = models.CharField(max_length=50)
#     npwp = models.CharField(max_length=50)
#     status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
#     created_at = models.DateTimeField(auto_now_add=True)
#     updated_at = models.DateTimeField(auto_now=True)