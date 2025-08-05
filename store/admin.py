from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Wishlist, WishlistItem

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'created_at']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    list_per_page = 20

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'category', 'price', 'stock_quantity', 'featured', 'available', 'created_at']
    list_filter = ['category', 'featured', 'available', 'created_at']
    list_editable = ['price', 'stock_quantity', 'featured', 'available']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name', 'description']
    raw_id_fields = ['category']
    list_per_page = 25
    date_hierarchy = 'created_at'
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'category', 'description')
        }),
        ('Pricing & Inventory', {
            'fields': ('price', 'stock_quantity', 'sizes', 'available', 'featured')
        }),
        ('Media', {
            'fields': ('image',)
        }),
    )

class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0

@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'total_items', 'total_price', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    inlines = [CartItemInline]
    
    def total_items(self, obj):
        return obj.total_items
    
    def total_price(self, obj):
        return f"${obj.total_price:.2f}"

class WishlistItemInline(admin.TabularInline):
    model = WishlistItem
    extra = 0

@admin.register(Wishlist)
class WishlistAdmin(admin.ModelAdmin):
    list_display = ['id', 'user', 'session_key', 'item_count', 'created_at']
    list_filter = ['created_at']
    search_fields = ['user__username', 'session_key']
    inlines = [WishlistItemInline]
    
    def item_count(self, obj):
        return obj.items.count()
