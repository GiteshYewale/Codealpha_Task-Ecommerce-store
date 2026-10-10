import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.test import Client
from django.urls import reverse
from store.models import Product, Order

def test_everything():
    print("==================================================")
    print("   FULL SYSTEM VERIFICATION & AUDIT (COMPREHENSIVE)   ")
    print("==================================================")

    client = Client()

    # 1. Admin Login via Username ('admin', 'admin123')
    login_admin_res = client.post('/admin/login/', {'username': 'admin', 'password': 'admin123', 'next': '/admin/'}, follow=True)
    assert login_admin_res.status_code == 200, f"Admin login failed with status {login_admin_res.status_code}"
    assert '_auth_user_id' in client.session, "Admin user session not created"
    assert "Site administration" in login_admin_res.content.decode('utf-8') or "Django administration" in login_admin_res.content.decode('utf-8')
    print("✅ Admin login via Username ('admin' / 'admin123') PASSED")
    client.logout()

    # 2. Admin Login via Email ('admin@codealpha.tech', 'admin123')
    login_email_res = client.post('/admin/login/', {'username': 'admin@codealpha.tech', 'password': 'admin123', 'next': '/admin/'}, follow=True)
    assert login_email_res.status_code == 200, f"Admin login via email failed with status {login_email_res.status_code}"
    assert '_auth_user_id' in client.session, "Admin email session not created"
    assert "Site administration" in login_email_res.content.decode('utf-8') or "Django administration" in login_email_res.content.decode('utf-8')
    print("✅ Admin login via Email ('admin@codealpha.tech' / 'admin123') PASSED")

    # 3. Access Django Admin Dashboard directly
    admin_index_res = client.get('/admin/')
    assert admin_index_res.status_code == 200, "Admin index failed"
    print("✅ Django Admin dashboard access PASSED")
    client.logout()

    # 4. Homepage / Product Catalog
    home_res = client.get('/')
    assert home_res.status_code == 200, "Homepage failed"
    print("✅ Homepage / Product Catalog view PASSED")

    # 5. Product Detail View
    p = Product.objects.first()
    detail_res = client.get(p.get_url())
    assert detail_res.status_code == 200, "Product detail failed"
    print(f"✅ Product detail page view for '{p.name}' PASSED")

    # 6. Add to Cart & View Cart
    add_res = client.get(reverse('add_cart', args=[p.id]))
    assert add_res.status_code == 302, "Add to cart redirect failed"
    cart_res = client.get(reverse('cart'))
    assert cart_res.status_code == 200, "Cart page failed"
    assert p.name in cart_res.content.decode('utf-8')
    print("✅ Shopping cart addition and display PASSED")

    # 7. Checkout Page
    checkout_res = client.get(reverse('checkout'))
    assert checkout_res.status_code == 200, "Checkout page failed"
    print("✅ Checkout page rendering PASSED")

    # 8. Order Processing
    order_data = {
        'full_name': 'Audit Tester',
        'email': 'tester@example.com',
        'phone': '555-111-2222',
        'address': '789 Market Street',
        'city': 'New York',
        'postal_code': '10001',
        'country': 'United States',
        'payment_method': 'Credit Card',
    }
    place_res = client.post(reverse('place_order'), data=order_data)
    assert place_res.status_code == 302, "Order placement redirect failed"
    assert Order.objects.filter(full_name='Audit Tester').exists(), "Order was not saved in DB"
    last_order = Order.objects.filter(full_name='Audit Tester').last()
    print(f"✅ Order processing & placement PASSED (Order #: {last_order.order_number})")

    # 9. Customer Authentication & Dashboard
    customer_login_res = client.post(reverse('login'), {'username': 'johndoe', 'password': 'password123'})
    assert customer_login_res.status_code == 302, "Customer login failed"
    dash_res = client.get(reverse('dashboard'))
    assert dash_res.status_code == 200, "Dashboard view failed"
    print("✅ Customer login & dashboard access PASSED")

    print("==================================================")
    print("🎉 ALL VERIFICATION TESTS PASSED (100% WORKING)!  ")
    print("==================================================")

if __name__ == '__main__':
    test_everything()
