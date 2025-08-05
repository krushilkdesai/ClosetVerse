import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from store.models import Category, Product

# Clear existing data
print("Clearing existing data...")
Product.objects.all().delete()
Category.objects.all().delete()

# Create categories with proper data
categories_data = [
    {
        'name': "Men's Clothing", 
        'slug': 'mens-clothing', 
        'description': 'Stylish and comfortable clothing for men including suits, shirts, and casual wear'
    },
    {
        'name': "Women's Clothing", 
        'slug': 'womens-clothing', 
        'description': 'Elegant and fashionable clothing for women including dresses, blouses, and professional wear'
    },
    {
        'name': 'Accessories', 
        'slug': 'accessories', 
        'description': 'Fashion accessories including bags, jewelry, watches, and belts'
    },
    {
        'name': 'Shoes', 
        'slug': 'shoes', 
        'description': 'Premium footwear for every occasion including boots, heels, sneakers, and formal shoes'
    },
    {
        'name': 'New Arrivals', 
        'slug': 'new-arrivals', 
        'description': 'Latest additions to our collection featuring the newest trends and styles'
    },
]

print("Creating categories...")
created_categories = {}
for cat_data in categories_data:
    category = Category.objects.create(**cat_data)
    created_categories[cat_data['slug']] = category
    print(f"✓ Created category: {category.name} ({category.slug})")

# Create sample products with Indian Rupee prices (1 USD ≈ 83 INR)
products_data = [
    # Men's Clothing
    {
        'name': 'Classic Business Suit',
        'slug': 'classic-business-suit',
        'category_slug': 'mens-clothing',
        'description': 'Professional tailored suit perfect for business meetings and formal events. Made from premium wool blend with modern fit.',
        'price': 49999.00,  # ₹49,999 (was $599.99)
        'sizes': 'S, M, L, XL, XXL',
        'featured': True,
    },
    {
        'name': 'Casual Cotton Polo',
        'slug': 'casual-cotton-polo',
        'category_slug': 'mens-clothing',
        'description': 'Comfortable cotton polo shirt for everyday wear. Breathable fabric with classic collar design.',
        'price': 6599.00,  # ₹6,599 (was $79.99)
        'sizes': 'S, M, L, XL, XXL',
        'featured': False,
    },
    {
        'name': 'Denim Jacket',
        'slug': 'denim-jacket',
        'category_slug': 'mens-clothing',
        'description': 'Vintage-style denim jacket with modern fit. Perfect for layering and casual outings.',
        'price': 10799.00,  # ₹10,799 (was $129.99)
        'sizes': 'S, M, L, XL',
        'featured': True,
    },
    {
        'name': 'Oxford Dress Shirt',
        'slug': 'oxford-dress-shirt',
        'category_slug': 'mens-clothing',
        'description': 'Classic oxford dress shirt with button-down collar. Essential for professional wardrobe.',
        'price': 7499.00,  # ₹7,499 (was $89.99)
        'sizes': 'S, M, L, XL, XXL',
        'featured': False,
    },
    {
        'name': 'Casual Chinos',
        'slug': 'casual-chinos',
        'category_slug': 'mens-clothing',
        'description': 'Comfortable chino pants perfect for casual and semi-formal occasions.',
        'price': 5799.00,  # ₹5,799 (was $69.99)
        'sizes': '30, 32, 34, 36, 38',
        'featured': False,
    },
    
    # Women's Clothing
    {
        'name': 'Elegant Evening Dress',
        'slug': 'elegant-evening-dress',
        'category_slug': 'womens-clothing',
        'description': 'Stunning evening dress crafted from premium silk. Perfect for special occasions and formal events.',
        'price': 29099.00,  # ₹29,099 (was $349.99)
        'sizes': 'XS, S, M, L, XL',
        'featured': True,
    },
    {
        'name': 'Casual Summer Blouse',
        'slug': 'casual-summer-blouse',
        'category_slug': 'womens-clothing',
        'description': 'Light and airy blouse perfect for summer days. Flowy design with delicate floral patterns.',
        'price': 7499.00,  # ₹7,499 (was $89.99)
        'sizes': 'XS, S, M, L, XL',
        'featured': False,
    },
    {
        'name': 'Professional Blazer',
        'slug': 'professional-blazer',
        'category_slug': 'womens-clothing',
        'description': 'Sophisticated blazer for the modern professional woman. Tailored fit with premium fabric.',
        'price': 16599.00,  # ₹16,599 (was $199.99)
        'sizes': 'XS, S, M, L, XL',
        'featured': True,
    },
    {
        'name': 'Midi Wrap Dress',
        'slug': 'midi-wrap-dress',
        'category_slug': 'womens-clothing',
        'description': 'Versatile wrap dress that flatters every figure. Perfect for both work and weekend.',
        'price': 12499.00,  # ₹12,499 (was $149.99)
        'sizes': 'XS, S, M, L, XL',
        'featured': False,
    },
    {
        'name': 'Silk Scarf Blouse',
        'slug': 'silk-scarf-blouse',
        'category_slug': 'womens-clothing',
        'description': 'Luxurious silk blouse with elegant scarf detail. Perfect for professional settings.',
        'price': 13299.00,  # ₹13,299 (was $159.99)
        'sizes': 'XS, S, M, L, XL',
        'featured': False,
    },
    
    # Accessories
    {
        'name': 'Designer Leather Handbag',
        'slug': 'designer-leather-handbag',
        'category_slug': 'accessories',
        'description': 'Luxurious leather handbag with gold hardware. Spacious interior with multiple compartments for organization.',
        'price': 24999.00,  # ₹24,999 (was $299.99)
        'sizes': 'One Size',
        'featured': True,
    },
    {
        'name': 'Classic Wristwatch',
        'slug': 'classic-wristwatch',
        'category_slug': 'accessories',
        'description': 'Timeless wristwatch with stainless steel band. Water-resistant with precise quartz movement.',
        'price': 20799.00,  # ₹20,799 (was $249.99)
        'sizes': 'One Size',
        'featured': False,
    },
    {
        'name': 'Silk Scarf Collection',
        'slug': 'silk-scarf-collection',
        'category_slug': 'accessories',
        'description': 'Premium silk scarves in various patterns. Perfect accessory to elevate any outfit.',
        'price': 6649.00,  # ₹6,649 (was $79.99)
        'sizes': 'One Size',
        'featured': True,
    },
    {
        'name': 'Leather Belt',
        'slug': 'leather-belt',
        'category_slug': 'accessories',
        'description': 'Genuine leather belt with classic buckle. Available in black and brown.',
        'price': 4999.00,  # ₹4,999 (was $59.99)
        'sizes': 'S, M, L, XL',
        'featured': False,
    },
    {
        'name': 'Pearl Necklace',
        'slug': 'pearl-necklace',
        'category_slug': 'accessories',
        'description': 'Elegant pearl necklace perfect for formal occasions. Classic design with lustrous pearls.',
        'price': 15799.00,  # ₹15,799 (was $189.99)
        'sizes': 'One Size',
        'featured': False,
    },
    
    # Shoes
    {
        'name': 'Premium Leather Boots',
        'slug': 'premium-leather-boots',
        'category_slug': 'shoes',
        'description': 'Handcrafted leather boots with superior comfort. Perfect for both casual and semi-formal occasions.',
        'price': 23299.00,  # ₹23,299 (was $279.99)
        'sizes': '6, 7, 8, 9, 10, 11, 12',
        'featured': True,
    },
    {
        'name': 'Athletic Running Shoes',
        'slug': 'athletic-running-shoes',
        'category_slug': 'shoes',
        'description': 'High-performance running shoes with advanced cushioning technology. Lightweight and breathable design.',
        'price': 13299.00,  # ₹13,299 (was $159.99)
        'sizes': '6, 7, 8, 9, 10, 11, 12',
        'featured': False,
    },
    {
        'name': 'Elegant High Heels',
        'slug': 'elegant-high-heels',
        'category_slug': 'shoes',
        'description': 'Sophisticated high heels that complement any formal outfit. Comfortable padding with stable heel design.',
        'price': 15799.00,  # ₹15,799 (was $189.99)
        'sizes': '5, 6, 7, 8, 9, 10',
        'featured': True,
    },
    {
        'name': 'Casual Sneakers',
        'slug': 'casual-sneakers',
        'category_slug': 'shoes',
        'description': 'Comfortable everyday sneakers with modern design. Perfect for casual wear and light activities.',
        'price': 8299.00,  # ₹8,299 (was $99.99)
        'sizes': '6, 7, 8, 9, 10, 11, 12',
        'featured': False,
    },
    {
        'name': 'Oxford Dress Shoes',
        'slug': 'oxford-dress-shoes',
        'category_slug': 'shoes',
        'description': 'Classic oxford dress shoes for formal occasions. Premium leather with traditional craftsmanship.',
        'price': 19099.00,  # ₹19,099 (was $229.99)
        'sizes': '7, 8, 9, 10, 11, 12',
        'featured': False,
    },
    
    # New Arrivals (mix from all categories)
    {
        'name': 'Limited Edition Sneakers',
        'slug': 'limited-edition-sneakers',
        'category_slug': 'new-arrivals',
        'description': 'Exclusive limited edition sneakers with unique colorway. Premium materials with modern street style.',
        'price': 16599.00,  # ₹16,599 (was $199.99)
        'sizes': '6, 7, 8, 9, 10, 11, 12',
        'featured': True,
    },
    {
        'name': 'Designer Crossbody Bag',
        'slug': 'designer-crossbody-bag',
        'category_slug': 'new-arrivals',
        'description': 'Trendy crossbody bag perfect for everyday use. Compact design with adjustable strap and premium finish.',
        'price': 12499.00,  # ₹12,499 (was $149.99)
        'sizes': 'One Size',
        'featured': True,
    },
    {
        'name': 'Sustainable Cotton T-Shirt',
        'slug': 'sustainable-cotton-tshirt',
        'category_slug': 'new-arrivals',
        'description': 'Eco-friendly t-shirt made from 100% organic cotton. Soft, comfortable, and environmentally conscious.',
        'price': 4149.00,  # ₹4,149 (was $49.99)
        'sizes': 'XS, S, M, L, XL, XXL',
        'featured': True,
    },
    {
        'name': 'Trendy Sunglasses',
        'slug': 'trendy-sunglasses',
        'category_slug': 'new-arrivals',
        'description': 'Fashion-forward sunglasses with UV protection. Lightweight frames with premium lenses.',
        'price': 10799.00,  # ₹10,799 (was $129.99)
        'sizes': 'One Size',
        'featured': False,
    },
    {
        'name': 'Modern Minimalist Watch',
        'slug': 'modern-minimalist-watch',
        'category_slug': 'new-arrivals',
        'description': 'Sleek minimalist watch with clean design. Perfect for contemporary fashion enthusiasts.',
        'price': 14949.00,  # ₹14,949 (was $179.99)
        'sizes': 'One Size',
        'featured': True,
    },
]

print("Creating products...")
created_products = 0
for product_data in products_data:
    try:
        category_slug = product_data.pop('category_slug')
        category = created_categories[category_slug]
        
        product_data['category'] = category
        
        product = Product.objects.create(**product_data)
        created_products += 1
        print(f"✓ Created product: {product.name} in {category.name} - ₹{product.price}")
        
    except KeyError as e:
        print(f"✗ Category not found for product: {product_data.get('name', 'Unknown')} - {e}")
    except Exception as e:
        print(f"✗ Error creating product {product_data.get('name', 'Unknown')}: {e}")

print("\n" + "="*60)
print("SUMMARY:")
print(f"Categories created: {Category.objects.count()}")
print(f"Products created: {Product.objects.count()}")
print("="*60)

# Display categories for verification
print("\nCategories in database:")
for category in Category.objects.all().order_by('name'):
    product_count = category.products.count()
    print(f"- {category.name} ({category.slug}) - {product_count} products")

print("\nSample data created successfully!")
print("All prices are now in Indian Rupees (₹)!")
