import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from store.models import Product, Category, Cart, CartItem, Order

def run_tests():
    print("--- RUNNING INTEGRATION TESTS FOR E-COMMERCE STORE ---")
    client = Client()

    # 1. Homepage / Store Catalog
    response = client.get(reverse('store'))
    assert response.status_code == 200, f"Store home failed with status {response.status_code}"
    print("✅ Store homepage test passed (200 OK)")

    # 2. Product Detail
    product = Product.objects.first()
    assert product is not None, "No products found in database"
    detail_url = reverse('product_detail', args=[product.category.slug, product.slug])
    response = client.get(detail_url)
    assert response.status_code == 200, f"Product detail failed with status {response.status_code}"
    print(f"✅ Product detail view test passed for '{product.name}' (200 OK)")

    # 3. Add to Cart
    add_cart_url = reverse('add_cart', args=[product.id])
    response = client.get(add_cart_url)
    assert response.status_code == 302, f"Add to cart redirect failed with status {response.status_code}"
    
    cart_url = reverse('cart')
    response = client.get(cart_url)
    assert response.status_code == 200, f"Cart view failed with status {response.status_code}"
    assert product.name in response.content.decode('utf-8'), "Product name missing in cart view"
    print("✅ Cart addition & display test passed")

    # 4. Checkout Page
    checkout_url = reverse('checkout')
    response = client.get(checkout_url)
    assert response.status_code == 200, f"Checkout view failed with status {response.status_code}"
    print("✅ Checkout view test passed")

    # 5. Place Order
    place_order_url = reverse('place_order')
    order_data = {
        'full_name': 'Test Buyer',
        'email': 'buyer@test.com',
        'phone': '1234567890',
        'address': '123 Test Street',
        'city': 'Test City',
        'postal_code': '12345',
        'country': 'United States',
        'payment_method': 'Credit Card',
    }
    response = client.post(place_order_url, data=order_data)
    assert response.status_code == 302, f"Place order redirect failed with status {response.status_code}"
    assert Order.objects.filter(full_name='Test Buyer').exists(), "Order was not saved in DB"
    last_order = Order.objects.filter(full_name='Test Buyer').last()
    print(f"✅ Order creation test passed! Generated Order #: {last_order.order_number}")

    # 6. User Login Test
    login_url = reverse('login')
    login_data = {'username': 'johndoe', 'password': 'password123'}
    response = client.post(login_url, data=login_data)
    assert response.status_code == 302, "User login failed"
    
    dashboard_url = reverse('dashboard')
    response = client.get(dashboard_url)
    assert response.status_code == 200, "Dashboard view failed after login"
    print("✅ User authentication & dashboard test passed")

    print("\n🎉 ALL E-COMMERCE INTEGRATION TESTS PASSED SUCCESSFULLY!")

if __name__ == '__main__':
    run_tests()
