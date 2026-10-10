import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Product

def fix():
    new_url = 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&auto=format&fit=crop&q=80'
    p = Product.objects.get(id=5)
    p.image_url = new_url
    p.save()
    print(f"✅ Updated Product [{p.id}] '{p.name}' image_url to: {new_url}")

if __name__ == '__main__':
    fix()
