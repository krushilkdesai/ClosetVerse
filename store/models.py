from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name_plural = 'Categories'
        ordering = ['name']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:category_products', kwargs={'slug': self.slug})

class Product(models.Model):
    SIZES = [
        ('XS', 'Extra Small'),
        ('S', 'Small'),
        ('M', 'Medium'),
        ('L', 'Large'),
        ('XL', 'Extra Large'),
        ('XXL', 'Double Extra Large'),
    ]

    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200, unique=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name='products')
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    image = models.ImageField(upload_to='products/', blank=True, null=True)
    sizes = models.CharField(max_length=100, help_text="Available sizes (comma-separated)")
    featured = models.BooleanField(default=False)
    available = models.BooleanField(default=True)
    stock_quantity = models.PositiveIntegerField(default=100)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('store:product_detail', kwargs={'slug': self.slug})

    def get_sizes_list(self):
        return [size.strip() for size in self.sizes.split(',') if size.strip()]

    @property
    def is_new_arrival(self):
        """Check if product is a new arrival (created within last 30 days)"""
        from django.utils import timezone
        from datetime import timedelta
        return self.created_at >= timezone.now() - timedelta(days=30)

class Cart(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        if self.user:
            return f"Cart for {self.user.username}"
        return f"Cart for session {self.session_key}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def total_price(self):
        return sum(item.get_total_price() for item in self.items.all())

class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField(default=1)
    size = models.CharField(max_length=10, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['cart', 'product', 'size']

    def __str__(self):
        return f"{self.quantity} x {self.product.name}"

    def get_total_price(self):
        return self.quantity * self.product.price

class Wishlist(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        if self.user:
            return f"Wishlist for {self.user.username}"
        return f"Wishlist for session {self.session_key}"

class WishlistItem(models.Model):
    wishlist = models.ForeignKey(Wishlist, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ['wishlist', 'product']

    def __str__(self):
        return f"{self.product.name} in wishlist"




class Order(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='orders')
    full_name = models.CharField(max_length=255)
    address = models.TextField()
    city = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    phone = models.CharField(max_length=20)
    payment_method = models.CharField(max_length=50)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)
    created_at = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=30, default='Placed')

class OrderItem(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()
    size = models.CharField(max_length=10, blank=True)
    total = models.DecimalField(max_digits=10, decimal_places=2)
