import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'ecommerce_project.settings')
django.setup()

from django.contrib.auth.models import User
from store.models import Category, Product, ProductReview, Order, OrderItem

def seed():
    print("Seeding E-Commerce Store Database...")

    # 1. Superuser & Test User
    admin_user, created = User.objects.get_or_create(username='admin', defaults={
        'email': 'admin@codealpha.tech',
        'is_staff': True,
        'is_superuser': True,
        'first_name': 'Admin',
        'last_name': 'User'
    })
    if created:
        admin_user.set_password('admin123')
        admin_user.save()
        print("Created Admin User (admin / admin123)")

    test_user, created = User.objects.get_or_create(username='johndoe', defaults={
        'email': 'john@example.com',
        'first_name': 'John',
        'last_name': 'Doe'
    })
    if created:
        test_user.set_password('password123')
        test_user.save()
        print("Created Test User (johndoe / password123)")

    # 2. Categories
    cat_electronics, _ = Category.objects.get_or_create(name='Electronics', slug='electronics', description='Gadgets, audio, and personal devices')
    cat_fashion, _ = Category.objects.get_or_create(name='Fashion & Apparel', slug='fashion-apparel', description='Modern clothing, shoes, and streetwear')
    cat_home, _ = Category.objects.get_or_create(name='Home & Living', slug='home-living', description='Smart appliances, furniture, and cozy decor')
    cat_fitness, _ = Category.objects.get_or_create(name='Sports & Fitness', slug='sports-fitness', description='Gym gear, wearables, and active lifestyle')

    # 3. Products
    products_data = [
        {
            'name': 'Antigravity Wireless ANC Headphones',
            'slug': 'antigravity-wireless-anc-headphones',
            'category': cat_electronics,
            'price': 199.99,
            'stock': 25,
            'featured': True,
            'description': 'Experience studio-grade active noise cancellation with 40-hour battery life, ultra-plush memory foam earcups, and crystal-clear acoustic drivers.',
            'image_url': 'https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'UltraSlim M3 OLED Laptop 15"',
            'slug': 'ultraslim-m3-oled-laptop-15',
            'category': cat_electronics,
            'price': 1299.00,
            'stock': 12,
            'featured': True,
            'description': 'Next-gen performance featuring a 3.5K OLED touchscreen display, 32GB LPDDR5 RAM, 1TB NVMe SSD, and all-day 18-hour battery efficiency.',
            'image_url': 'https://images.unsplash.com/photo-1496181133206-80ce9b88a853?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'ProFit Smart Fitness Watch',
            'slug': 'profit-smart-fitness-watch',
            'category': cat_fitness,
            'price': 149.50,
            'stock': 40,
            'featured': True,
            'description': 'Continuous heart rate monitoring, built-in GPS tracking, 50m water resistance, and advanced sleep telemetry wrapped in aerospace aluminum.',
            'image_url': 'https://images.unsplash.com/photo-1523275335684-37898b6baf30?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Urban Minimalist Leather Backpack',
            'slug': 'urban-minimalist-leather-backpack',
            'category': cat_fashion,
            'price': 89.99,
            'stock': 18,
            'featured': False,
            'description': 'Crafted from full-grain genuine leather with dedicated padded 16-inch laptop compartment and hidden anti-theft security pocket.',
            'image_url': 'https://images.unsplash.com/photo-1553062407-98eeb64c6a62?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Ergonomic Mesh Office Chair',
            'slug': 'ergonomic-mesh-office-chair',
            'category': cat_home,
            'price': 249.99,
            'stock': 15,
            'featured': True,
            'description': '3D adjustable lumbar support, 4D armrests, high-breathability mesh backrest, and heavy-duty smooth roller wheels for peak productivity.',
            'image_url': 'https://images.unsplash.com/photo-1586023492125-27b2c045efd7?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Ceramic Smart Temperature Mug',
            'slug': 'ceramic-smart-temperature-mug',
            'category': cat_home,
            'price': 69.95,
            'stock': 30,
            'featured': False,
            'description': 'Keep your coffee or tea at your precise preferred drinking temperature for up to 3 hours off charging coaster or all day on coaster.',
            'image_url': 'https://images.unsplash.com/photo-1514432324607-a09d9b4aefdd?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Mechanical RGB Wireless Keyboard',
            'slug': 'mechanical-rgb-wireless-keyboard',
            'category': cat_electronics,
            'price': 119.00,
            'stock': 22,
            'featured': False,
            'description': 'Hot-swappable tactile switches, per-key RGB backlighting, tri-mode connectivity (Bluetooth, 2.4Ghz, Type-C), and anodized aluminum chassis.',
            'image_url': 'https://images.unsplash.com/photo-1587829741301-dc798b83add3?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Classic Polarized Sunglasses',
            'slug': 'classic-polarized-sunglasses',
            'category': cat_fashion,
            'price': 45.00,
            'stock': 50,
            'featured': False,
            'description': 'UV400 protection lenses with durable lightweight acetate frames for outdoor adventures and effortless everyday style.',
            'image_url': 'https://images.unsplash.com/photo-1511499767150-a48a237f0083?w=800&auto=format&fit=crop&q=80'
        },
    ]

    for p_info in products_data:
        p, created = Product.objects.get_or_create(
            slug=p_info['slug'],
            defaults={
                'name': p_info['name'],
                'category': p_info['category'],
                'price': p_info['price'],
                'stock': p_info['stock'],
                'featured': p_info['featured'],
                'description': p_info['description'],
                'image_url': p_info['image_url'],
                'is_available': True
            }
        )
        if created:
            print(f"Added product: {p.name}")
            # Add sample review
            ProductReview.objects.create(
                product=p,
                user=test_user,
                rating=5,
                subject="Outstanding quality!",
                comment="Received this product yesterday and the build quality exceeds all expectations. Very satisfied with my purchase!"
            )

    print("Seeding complete! Store is ready.")

if __name__ == '__main__':
    seed()
