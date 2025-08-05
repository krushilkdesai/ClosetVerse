import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from store.models import Product

def update_prices_to_inr():
    """Update all existing product prices to Indian Rupees"""
    
    # Price conversion mapping (USD to INR approximately 1:83)
    price_mapping = {
        599.99: 49999.00,   # Classic Business Suit
        79.99: 6599.00,     # Casual Cotton Polo
        129.99: 10799.00,   # Denim Jacket
        89.99: 7499.00,     # Oxford Dress Shirt
        69.99: 5799.00,     # Casual Chinos
        349.99: 29099.00,   # Elegant Evening Dress
        199.99: 16599.00,   # Professional Blazer
        149.99: 12499.00,   # Midi Wrap Dress / Designer Crossbody Bag
        159.99: 13299.00,   # Silk Scarf Blouse / Athletic Running Shoes
        299.99: 24999.00,   # Designer Leather Handbag
        249.99: 20799.00,   # Classic Wristwatch
        59.99: 4999.00,     # Leather Belt
        189.99: 15799.00,   # Pearl Necklace / Elegant High Heels
        279.99: 23299.00,   # Premium Leather Boots
        99.99: 8299.00,     # Casual Sneakers
        229.99: 19099.00,   # Oxford Dress Shoes
        49.99: 4149.00,     # Sustainable Cotton T-Shirt
        179.99: 14949.00,   # Modern Minimalist Watch
    }
    
    products = Product.objects.all()
    updated_count = 0
    
    for product in products:
        old_price = float(product.price)
        
        # Find matching price in mapping
        new_price = None
        for usd_price, inr_price in price_mapping.items():
            if abs(old_price - usd_price) < 0.01:  # Allow for small floating point differences
                new_price = inr_price
                break
        
        if new_price:
            product.price = new_price
            product.save()
            updated_count += 1
            print(f"✓ Updated {product.name}: ${old_price} → ₹{new_price}")
        else:
            # If no exact match, convert using 1 USD = 83 INR
            converted_price = round(old_price * 83, 0)
            product.price = converted_price
            product.save()
            updated_count += 1
            print(f"✓ Converted {product.name}: ${old_price} → ₹{converted_price}")
    
    print(f"\n✅ Updated {updated_count} products with Indian Rupee prices!")

if __name__ == "__main__":
    print("Converting prices to Indian Rupees...")
    update_prices_to_inr()
    print("Price conversion completed!")
