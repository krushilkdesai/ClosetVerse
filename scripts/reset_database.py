import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'fashion_store.settings')
django.setup()

from django.core.management import execute_from_command_line
import sys

def reset_database():
    """Reset the database and recreate everything"""
    print("Resetting database...")
    
    # Delete the database file
    try:
        if os.path.exists('db.sqlite3'):
            os.remove('db.sqlite3')
            print("✓ Deleted existing database")
    except Exception as e:
        print(f"Warning: Could not delete database: {e}")
    
    # Delete migration files (except __init__.py)
    migrations_dir = 'store/migrations'
    if os.path.exists(migrations_dir):
        for file in os.listdir(migrations_dir):
            if file.endswith('.py') and file != '__init__.py':
                try:
                    os.remove(os.path.join(migrations_dir, file))
                    print(f"✓ Deleted migration: {file}")
                except Exception as e:
                    print(f"Warning: Could not delete {file}: {e}")
    
    # Create new migrations
    print("Creating new migrations...")
    execute_from_command_line(['manage.py', 'makemigrations'])
    
    # Apply migrations
    print("Applying migrations...")
    execute_from_command_line(['manage.py', 'migrate'])
    
    # Create superuser (optional)
    print("Database reset completed!")
    print("Run 'python scripts/create_sample_data.py' to add sample data")

if __name__ == "__main__":
    reset_database()
