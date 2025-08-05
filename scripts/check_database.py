import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from store.models import Category, Product

print("DATABASE STATUS CHECK")
print("="*50)

print(f"Total Categories: {Category.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

print("\nCategories:")
for category in Category.objects.all():
    product_count = category.products.count()
    print(f"  - {category.name} ({category.slug}) - {product_count} products")

print("\nProducts by Category:")
for category in Category.objects.all():
    products = category.products.all()
    print(f"\n{category.name}:")
    for product in products:
        print(f"  - {product.name} (${product.price})")

if Category.objects.count() == 0:
    print("\n⚠️  NO CATEGORIES FOUND!")
    print("Run: python scripts/create_sample_data.py")

if Product.objects.count() == 0:
    print("\n⚠️  NO PRODUCTS FOUND!")
    print("Run: python scripts/create_sample_data.py")
