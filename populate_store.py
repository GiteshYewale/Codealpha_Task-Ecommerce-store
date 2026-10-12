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
    cat_beauty, _ = Category.objects.get_or_create(name='Beauty & Personal Care', slug='beauty-personal-care', description='Skincare, fragrance, and daily self-care essentials')
    cat_kitchen, _ = Category.objects.get_or_create(name='Kitchen & Dining', slug='kitchen-dining', description='Cookware, appliances, and tabletop essentials')
    cat_books, _ = Category.objects.get_or_create(name='Books & Stationery', slug='books-stationery', description='Bestselling reads, journals, and desk supplies')
    cat_toys, _ = Category.objects.get_or_create(name='Toys & Games', slug='toys-games', description='Board games, RC toys, and fun for all ages')

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
        {
            'name': 'ProShot 4K Mirrorless Camera',
            'slug': 'proshot-4k-mirrorless-camera',
            'category': cat_electronics,
            'price': 899.00,
            'stock': 10,
            'featured': True,
            'description': 'Capture cinematic detail with a 24MP sensor, 4K/60fps video, in-body stabilization, and a fast hybrid autofocus system.',
            'image_url': 'https://images.unsplash.com/photo-1516035069371-29a1b244cc32?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'AeroSound Portable Bluetooth Speaker',
            'slug': 'aerosound-portable-bluetooth-speaker',
            'category': cat_electronics,
            'price': 79.99,
            'stock': 35,
            'featured': False,
            'description': '360-degree room-filling sound, 24-hour playtime, IPX7 waterproofing, and USB-C fast charging in a rugged travel-ready shell.',
            'image_url': 'https://images.unsplash.com/photo-1608043152269-423dbba4e7e1?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'CloudStep Running Sneakers',
            'slug': 'cloudstep-running-sneakers',
            'category': cat_fashion,
            'price': 120.00,
            'stock': 28,
            'featured': True,
            'description': 'Responsive foam midsole, breathable engineered knit upper, and a grippy rubber outsole built for daily miles and all-day comfort.',
            'image_url': 'https://images.unsplash.com/photo-1542291026-7eec264c27ff?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Milano Leather Crossbody Bag',
            'slug': 'milano-leather-crossbody-bag',
            'category': cat_fashion,
            'price': 135.00,
            'stock': 16,
            'featured': False,
            'description': 'Hand-finished Italian leather with an adjustable strap, magnetic closure, and multiple compartments for seamless city days.',
            'image_url': 'https://images.unsplash.com/photo-1584917865442-de89df76afd3?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Barista Pro Espresso Machine',
            'slug': 'barista-pro-espresso-machine',
            'category': cat_kitchen,
            'price': 349.00,
            'stock': 14,
            'featured': True,
            'description': '15-bar pump pressure, integrated conical burr grinder, and a professional steam wand for silky microfoam at home.',
            'image_url': 'https://images.unsplash.com/photo-1517668808822-9ebb02f2a0e6?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Scandinavian Ceramic Dinner Set',
            'slug': 'scandinavian-ceramic-dinner-set',
            'category': cat_kitchen,
            'price': 89.00,
            'stock': 20,
            'featured': False,
            'description': 'A 16-piece stoneware set with a matte reactive glaze finish — dishwasher, microwave, and oven safe for everyday dining.',
            'image_url': 'https://images.unsplash.com/photo-1603199506016-b9a594b593c0?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'The Art of Focus (Hardcover)',
            'slug': 'the-art-of-focus-hardcover',
            'category': cat_books,
            'price': 24.99,
            'stock': 45,
            'featured': False,
            'description': 'A practical guide to deep work and distraction-free living, packed with research-backed strategies for sustained attention.',
            'image_url': 'https://images.unsplash.com/photo-1512820790803-83ca734da794?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Premium Vegan Leather Journal',
            'slug': 'premium-vegan-leather-journal',
            'category': cat_books,
            'price': 29.00,
            'stock': 60,
            'featured': False,
            'description': 'A5 dotted notebook with 120gsm bleed-resistant pages, an elastic closure, ribbon marker, and a soft-touch vegan leather cover.',
            'image_url': 'https://images.unsplash.com/photo-1531346878377-a5be20888e57?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Galactic Strategy Board Game',
            'slug': 'galactic-strategy-board-game',
            'category': cat_toys,
            'price': 49.99,
            'stock': 26,
            'featured': True,
            'description': 'Build your fleet, colonize planets, and outwit rivals in this 2-5 player strategy game with 60-minute sessions and endless replayability.',
            'image_url': 'https://images.unsplash.com/photo-1606503153255-59d8b8b82176?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Drift RC Stunt Car',
            'slug': 'drift-rc-stunt-car',
            'category': cat_toys,
            'price': 64.99,
            'stock': 32,
            'featured': False,
            'description': '2.4GHz dual-motor remote control car with 360-degree flips, all-terrain tires, and a rechargeable battery for 30 minutes of play.',
            'image_url': 'https://images.unsplash.com/photo-1594787318286-3d835c1d207f?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'UltraSculpt Yoga Mat Pro',
            'slug': 'ultrasculpt-yoga-mat-pro',
            'category': cat_fitness,
            'price': 45.00,
            'stock': 38,
            'featured': False,
            'description': 'Extra-thick 6mm TPE mat with a non-slip textured surface, alignment lines, and a carrying strap — eco-friendly and odor-free.',
            'image_url': 'https://images.unsplash.com/photo-1544367567-0f2fcb009e0b?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Radiance Vitamin C Serum',
            'slug': 'radiance-vitamin-c-serum',
            'category': cat_beauty,
            'price': 32.00,
            'stock': 55,
            'featured': True,
            'description': 'A brightening 20% vitamin C serum with hyaluronic acid and vitamin E to even tone and boost daily radiance. Dermatologist tested.',
            'image_url': 'https://images.unsplash.com/photo-1556228578-8c89e6adf883?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'HydraBoost Hyaluronic Moisturizer',
            'slug': 'hydraboost-hyaluronic-moisturizer',
            'category': cat_beauty,
            'price': 27.50,
            'stock': 48,
            'featured': False,
            'description': 'A lightweight gel-cream with multi-weight hyaluronic acid that delivers 72-hour hydration and a smooth, non-greasy finish.',
            'image_url': 'https://images.unsplash.com/photo-1556228720-195a672e8a03?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Silk Repair Argan Hair Oil',
            'slug': 'silk-repair-argan-hair-oil',
            'category': cat_beauty,
            'price': 22.00,
            'stock': 52,
            'featured': False,
            'description': 'Cold-pressed Moroccan argan oil blended with vitamin E to tame frizz, add shine, and repair split ends without a heavy feel.',
            'image_url': 'https://images.unsplash.com/photo-1608248597279-f99d160bfcbc?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Velvet Matte Lipstick Trio',
            'slug': 'velvet-matte-lipstick-trio',
            'category': cat_beauty,
            'price': 34.00,
            'stock': 40,
            'featured': False,
            'description': 'Three universally flattering matte shades with creamy, long-wearing pigment and nourishing shea butter. Cruelty-free and vegan.',
            'image_url': 'https://images.unsplash.com/photo-1586495777744-4413f21062fa?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Cedar & Amber Eau de Parfum',
            'slug': 'cedar-amber-eau-de-parfum',
            'category': cat_beauty,
            'price': 78.00,
            'stock': 30,
            'featured': True,
            'description': 'A warm woody signature scent with notes of cedar, amber, and bergamot that lasts up to 10 hours. 50ml eau de parfum.',
            'image_url': 'https://images.unsplash.com/photo-1596462502278-27bfdc403348?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Executive Fountain Pen Set',
            'slug': 'executive-fountain-pen-set',
            'category': cat_books,
            'price': 42.00,
            'stock': 35,
            'featured': False,
            'description': 'A weighted brass fountain pen with a smooth medium nib, gift box, and two ink cartridges for a refined writing experience.',
            'image_url': 'https://images.unsplash.com/photo-1583485088034-697b5bc54ccd?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Daily Focus Planner 2026',
            'slug': 'daily-focus-planner-2026',
            'category': cat_books,
            'price': 19.99,
            'stock': 55,
            'featured': False,
            'description': 'An undated weekly and daily planner with goal trackers, habit grids, and monthly overviews to keep your year organized.',
            'image_url': 'https://images.unsplash.com/photo-1506784983877-45594efa4cbe?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Minimalist Wooden Desk Organizer',
            'slug': 'minimalist-wooden-desk-organizer',
            'category': cat_books,
            'price': 36.50,
            'stock': 24,
            'featured': False,
            'description': 'Solid walnut desk organizer with compartments for pens, a phone slot, and a note card stand to keep any workspace tidy.',
            'image_url': 'https://images.unsplash.com/photo-1518455027359-f3f8164ba6bd?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Heritage Denim Jacket',
            'slug': 'heritage-denim-jacket',
            'category': cat_fashion,
            'price': 89.00,
            'stock': 22,
            'featured': True,
            'description': 'A timeless mid-wash denim jacket in durable cotton with a tailored fit, brass hardware, and a classic four-pocket design.',
            'image_url': 'https://images.unsplash.com/photo-1523206489230-c012c64b2b48?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Minimalist Bedside Table Lamp',
            'slug': 'minimalist-bedside-table-lamp',
            'category': cat_home,
            'price': 54.00,
            'stock': 26,
            'featured': False,
            'description': 'A warm dimmable LED desk lamp with a matte ceramic base, touch controls, and three color temperatures for reading or relaxing.',
            'image_url': 'https://images.unsplash.com/photo-1507473885765-e6ed057f782c?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Handwoven Cotton Throw Blanket',
            'slug': 'handwoven-cotton-throw-blanket',
            'category': cat_home,
            'price': 49.00,
            'stock': 33,
            'featured': False,
            'description': 'A soft, breathable 100% cotton throw with a subtle fringe, perfect for layering on a sofa or bed in any season.',
            'image_url': 'https://images.unsplash.com/photo-1584100936595-c0654b55a2e2?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Aromatherapy Essential Oil Diffuser',
            'slug': 'aromatherapy-essential-oil-diffuser',
            'category': cat_home,
            'price': 39.95,
            'stock': 29,
            'featured': False,
            'description': 'An ultrasonic 300ml diffuser with 7 ambient light settings, auto shut-off, and whisper-quiet operation for calm, scented rooms.',
            'image_url': 'https://images.unsplash.com/photo-1602928298849-325cec8771c0?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': "Chef's Stainless Steel Knife Set",
            'slug': 'chefs-stainless-steel-knife-set',
            'category': cat_kitchen,
            'price': 99.00,
            'stock': 18,
            'featured': True,
            'description': 'A 5-piece German stainless steel knife set with ergonomic handles, a bamboo block, and razor-sharp precision-forged blades.',
            'image_url': 'https://images.unsplash.com/photo-1594385208974-2e75f8d7bb48?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Cast Iron Dutch Oven 5.5 Qt',
            'slug': 'cast-iron-dutch-oven-5-5-qt',
            'category': cat_kitchen,
            'price': 129.00,
            'stock': 16,
            'featured': False,
            'description': 'Enameled cast iron dutch oven for slow cooking, baking, and braising. Even heat retention and oven safe to 500 F.',
            'image_url': 'https://images.unsplash.com/photo-1585515320310-259814833e62?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Borosilicate Glass Storage Set',
            'slug': 'borosilicate-glass-storage-set',
            'category': cat_kitchen,
            'price': 44.50,
            'stock': 34,
            'featured': False,
            'description': 'A 10-piece airtight glass food storage set with snap-lock lids that are leak-proof, oven-safe, and stackable for tidy kitchens.',
            'image_url': 'https://images.unsplash.com/photo-1610701596007-11502861dcfa?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Adjustable Dumbbell Set 5-25kg',
            'slug': 'adjustable-dumbbell-set-5-25kg',
            'category': cat_fitness,
            'price': 219.00,
            'stock': 12,
            'featured': True,
            'description': 'A space-saving pair of adjustable dumbbells with quick-lock plates, replacing 15 sets of weights for full-body training.',
            'image_url': 'https://images.unsplash.com/photo-1571019613454-1cb2f99b2d8b?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Insulated Stainless Steel Water Bottle',
            'slug': 'insulated-stainless-steel-water-bottle',
            'category': cat_fitness,
            'price': 29.99,
            'stock': 60,
            'featured': False,
            'description': 'A 32oz double-wall vacuum bottle that keeps drinks cold for 24 hours or hot for 12, with a leak-proof lid and powder-coated grip.',
            'image_url': 'https://images.unsplash.com/photo-1602143407151-7111542de6e8?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Resistance Bands Set (5 Levels)',
            'slug': 'resistance-bands-set-5-levels',
            'category': cat_fitness,
            'price': 24.99,
            'stock': 44,
            'featured': False,
            'description': 'Five color-coded latex bands from light to extra-heavy, complete with door anchor, handles, and an ankle strap for home workouts.',
            'image_url': 'https://images.unsplash.com/photo-1598971639058-fab3c3109a00?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'Wooden Building Blocks Set',
            'slug': 'wooden-building-blocks-set',
            'category': cat_toys,
            'price': 39.99,
            'stock': 30,
            'featured': False,
            'description': '100 sustainably sourced hardwood blocks with non-toxic water-based paint to spark creativity and early learning.',
            'image_url': 'https://images.unsplash.com/photo-1587654780291-39c9404d746b?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': 'STEM Robotics Building Kit',
            'slug': 'stem-robotics-building-kit',
            'category': cat_toys,
            'price': 74.99,
            'stock': 20,
            'featured': True,
            'description': 'A hands-on 12-in-1 robotics kit that teaches coding and mechanics through buildable, app-controlled robots. Ages 8+.',
            'image_url': 'https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&auto=format&fit=crop&q=80'
        },
        {
            'name': '1000-Piece Landscape Jigsaw Puzzle',
            'slug': '1000-piece-landscape-jigsaw-puzzle',
            'category': cat_toys,
            'price': 21.99,
            'stock': 42,
            'featured': False,
            'description': 'A precision-cut 1000-piece puzzle with a vibrant landscape artwork, made from recycled board with a linen finish.',
            'image_url': 'https://images.unsplash.com/photo-1610890716171-6b1bb98ffd09?w=800&auto=format&fit=crop&q=80'
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
