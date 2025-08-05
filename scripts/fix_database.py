import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from django.db import connection

def add_stock_quantity_column():
    """Add stock_quantity column to store_product table if it doesn't exist"""
    with connection.cursor() as cursor:
        try:
            # Check if column exists
            cursor.execute("PRAGMA table_info(store_product)")
            columns = [column[1] for column in cursor.fetchall()]
            
            if 'stock_quantity' not in columns:
                print("Adding stock_quantity column...")
                cursor.execute("ALTER TABLE store_product ADD COLUMN stock_quantity INTEGER DEFAULT 100")
                print("✓ stock_quantity column added successfully")
            else:
                print("✓ stock_quantity column already exists")
                
        except Exception as e:
            print(f"Error: {e}")

def add_cart_tables():
    """Create cart and wishlist tables if they don't exist"""
    with connection.cursor() as cursor:
        try:
            # Check if cart table exists
            cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name='store_cart'")
            if not cursor.fetchone():
                print("Creating cart tables...")
                
                # Create Cart table
                cursor.execute("""
                    CREATE TABLE store_cart (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NULL,
                        session_key VARCHAR(40) NULL,
                        created_at DATETIME NOT NULL,
                        updated_at DATETIME NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES auth_user (id)
                    )
                """)
                
                # Create CartItem table
                cursor.execute("""
                    CREATE TABLE store_cartitem (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        cart_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        quantity INTEGER NOT NULL,
                        size VARCHAR(10) NOT NULL DEFAULT '',
                        created_at DATETIME NOT NULL,
                        FOREIGN KEY (cart_id) REFERENCES store_cart (id),
                        FOREIGN KEY (product_id) REFERENCES store_product (id),
                        UNIQUE (cart_id, product_id, size)
                    )
                """)
                
                # Create Wishlist table
                cursor.execute("""
                    CREATE TABLE store_wishlist (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        user_id INTEGER NULL,
                        session_key VARCHAR(40) NULL,
                        created_at DATETIME NOT NULL,
                        FOREIGN KEY (user_id) REFERENCES auth_user (id)
                    )
                """)
                
                # Create WishlistItem table
                cursor.execute("""
                    CREATE TABLE store_wishlistitem (
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        wishlist_id INTEGER NOT NULL,
                        product_id INTEGER NOT NULL,
                        created_at DATETIME NOT NULL,
                        FOREIGN KEY (wishlist_id) REFERENCES store_wishlist (id),
                        FOREIGN KEY (product_id) REFERENCES store_product (id),
                        UNIQUE (wishlist_id, product_id)
                    )
                """)
                
                print("✓ Cart and wishlist tables created successfully")
            else:
                print("✓ Cart tables already exist")
                
        except Exception as e:
            print(f"Error creating tables: {e}")

if __name__ == "__main__":
    print("Fixing database schema...")
    add_stock_quantity_column()
    add_cart_tables()
    print("Database fix completed!")
