import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from store.models import Category, Product

print("CATEGORY CHECK")
print("="*50)

print(f"Total Categories: {Category.objects.count()}")
print(f"Total Products: {Product.objects.count()}")

print("\nAll Categories in Database:")
categories = Category.objects.all().order_by('name')
if categories:
    for category in categories:
        product_count = category.products.count()
        print(f"  ✓ {category.name} ({category.slug}) - {product_count} products")
else:
    print("  ⚠️  NO CATEGORIES FOUND!")

print("\nChecking specific category slugs:")
required_slugs = ['mens-clothing', 'womens-clothing', 'accessories', 'shoes', 'new-arrivals']
for slug in required_slugs:
    try:
        category = Category.objects.get(slug=slug)
        print(f"  ✓ {slug} -> {category.name}")
    except Category.DoesNotExist:
        print(f"  ✗ {slug} -> NOT FOUND")

print("\nProducts by Category:")
for category in categories:
    products = category.products.all()[:3]  # Show first 3 products
    print(f"\n{category.name} ({category.products.count()} total):")
    for product in products:
        print(f"  - {product.name} (${product.price})")
    if category.products.count() > 3:
        print(f"  ... and {category.products.count() - 3} more")

if Category.objects.count() == 0:
    print("\n" + "="*50)
    print("⚠️  DATABASE IS EMPTY!")
    print("Run: python scripts/create_sample_data.py")
    print("="*50)
else:
    print("\n" + "="*50)
    print("✅ Database looks good!")
    print("="*50)
