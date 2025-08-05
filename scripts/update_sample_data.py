import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from store.models import Product

def update_products_with_stock():
    """Update all products with stock quantity"""
    products = Product.objects.all()
    
    for product in products:
        if not hasattr(product, 'stock_quantity') or product.stock_quantity is None:
            # Set different stock levels for variety
            if product.featured:
                product.stock_quantity = 50  # Featured items have moderate stock
            elif product.is_new_arrival:
                product.stock_quantity = 25  # New arrivals have limited stock
            else:
                product.stock_quantity = 100  # Regular items have full stock
            
            product.save()
            print(f"✓ Updated {product.name} with stock quantity: {product.stock_quantity}")

if __name__ == "__main__":
    print("Updating products with stock quantities...")
    update_products_with_stock()
    print("Stock quantities updated successfully!")
