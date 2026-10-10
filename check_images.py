import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Product

def check_all_images():
    print("--- CHECKING PRODUCT IMAGES ---")
    products = Product.objects.all()
    for p in products:
        img_src = p.get_image()
        print(f"ID: {p.id} | Name: {p.name}")
        print(f"   Image Field: {p.image}")
        print(f"   Image URL: {p.image_url}")
        print(f"   Effective URL: {img_src}")
        print("-" * 50)

if __name__ == '__main__':
    check_all_images()
