import urllib.request
import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from store.models import Product

def test_urls():
    products = Product.objects.all()
    headers = {'User-Agent': 'Mozilla/5.0'}
    print("--- TESTING HTTP AVAILABILITY OF PRODUCT IMAGES ---")
    for p in products:
        url = p.get_image()
        try:
            req = urllib.request.Request(url, headers=headers)
            with urllib.request.urlopen(req, timeout=5) as response:
                print(f"Product [{p.id}] '{p.name}': Status {response.status} OK")
        except Exception as e:
            print(f"❌ BROKEN IMAGE! Product [{p.id}] '{p.name}': URL={url} -> Error: {e}")

if __name__ == '__main__':
    test_urls()
