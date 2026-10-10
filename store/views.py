from django.shortcuts import render, get_object_or_404, redirect
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.exceptions import ObjectDoesNotExist
from decimal import Decimal
import datetime
import uuid

from .models import Category, Product, Cart, CartItem, Order, OrderItem, ProductReview


def _cart_id(request):
    cart = request.session.session_key
    if not cart:
        cart = request.session.create()
    return cart


def store(request, category_slug=None):
    categories = None
    products = None
    category = None

    sort_by = request.GET.get('sort', 'newest')

    if category_slug != None:
        category = get_object_or_404(Category, slug=category_slug)
        products = Product.objects.filter(category=category, is_available=True)
    else:
        products = Product.objects.all().filter(is_available=True)

    # Sorting
    if sort_by == 'price_low':
        products = products.order_by('price')
    elif sort_by == 'price_high':
        products = products.order_by('-price')
    elif sort_by == 'name':
        products = products.order_by('name')
    else:
        products = products.order_by('-created_at')

    product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'current_category': category,
        'sort_by': sort_by,
    }
    return render(request, 'store/store.html', context)


def product_detail(request, category_slug, product_slug):
    try:
        single_product = Product.objects.get(category__slug=category_slug, slug=product_slug)
        in_cart = CartItem.objects.filter(cart__cart_id=_cart_id(request), product=single_product).exists()
    except Exception as e:
        raise e

    reviews = ProductReview.objects.filter(product=single_product).order_by('-created_at')
    related_products = Product.objects.filter(category=single_product.category).exclude(id=single_product.id)[:4]

    context = {
        'product': single_product,
        'in_cart': in_cart,
        'reviews': reviews,
        'related_products': related_products,
    }
    return render(request, 'store/product_detail.html', context)


def search(request):
    products = []
    product_count = 0
    keyword = request.GET.get('keyword', '')
    if keyword:
        products = Product.objects.order_by('-created_at').filter(
            Q(description__icontains=keyword) | Q(name__icontains=keyword)
        )
        product_count = products.count()

    context = {
        'products': products,
        'product_count': product_count,
        'keyword': keyword,
    }
    return render(request, 'store/store.html', context)


def add_cart(request, product_id):
    current_user = request.user
    product = get_object_or_404(Product, id=product_id)

    qty = 1
    if request.method == 'POST':
        try:
            qty = int(request.POST.get('quantity', 1))
        except ValueError:
            qty = 1

    if current_user.is_authenticated:
        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            user=current_user,
            defaults={'quantity': qty}
        )
        if not created:
            cart_item.quantity += qty
            cart_item.save()
    else:
        try:
            cart = Cart.objects.get(cart_id=_cart_id(request))
        except Cart.DoesNotExist:
            cart = Cart.objects.create(cart_id=_cart_id(request))
        cart.save()

        cart_item, created = CartItem.objects.get_or_create(
            product=product,
            cart=cart,
            defaults={'quantity': qty}
        )
        if not created:
            cart_item.quantity += qty
            cart_item.save()

    messages.success(request, f"Added '{product.name}' to your shopping cart!")
    
    next_url = request.META.get('HTTP_REFERER')
    if next_url and 'cart' not in next_url:
        return redirect(next_url)
    return redirect('cart')


def remove_cart(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        
        if cart_item.quantity > 1:
            cart_item.quantity -= 1
            cart_item.save()
        else:
            cart_item.delete()
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def remove_cart_item(request, product_id, cart_item_id):
    product = get_object_or_404(Product, id=product_id)
    try:
        if request.user.is_authenticated:
            cart_item = CartItem.objects.get(product=product, user=request.user, id=cart_item_id)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_item = CartItem.objects.get(product=product, cart=cart, id=cart_item_id)
        cart_item.delete()
        messages.info(request, f"Removed '{product.name}' from your cart.")
    except CartItem.DoesNotExist:
        pass
    return redirect('cart')


def cart(request, total=Decimal('0.00'), quantity=0, cart_items=None):
    tax = Decimal('0.00')
    grand_total = Decimal('0.00')
    shipping = Decimal('0.00')
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        if total > Decimal('0.00'):
            tax = (Decimal('0.02') * total).quantize(Decimal('0.01')) # 2% tax
            shipping = Decimal('0.00') if total >= Decimal('200.00') else Decimal('15.00')
            grand_total = total + tax + shipping

    except ObjectDoesNotExist:
        pass

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'store/cart.html', context)


def checkout(request, total=Decimal('0.00'), quantity=0, cart_items=None):
    tax = Decimal('0.00')
    grand_total = Decimal('0.00')
    shipping = Decimal('0.00')
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.get(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart, is_active=True)

        for cart_item in cart_items:
            total += (cart_item.product.price * cart_item.quantity)
            quantity += cart_item.quantity

        if total > Decimal('0.00'):
            tax = (Decimal('0.02') * total).quantize(Decimal('0.01'))
            shipping = Decimal('0.00') if total >= Decimal('200.00') else Decimal('15.00')
            grand_total = total + tax + shipping

    except ObjectDoesNotExist:
        return redirect('store')

    if not cart_items or len(cart_items) == 0:
        messages.warning(request, "Your shopping cart is empty.")
        return redirect('store')

    context = {
        'total': total,
        'quantity': quantity,
        'cart_items': cart_items,
        'tax': tax,
        'shipping': shipping,
        'grand_total': grand_total,
    }
    return render(request, 'store/checkout.html', context)


def place_order(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            try:
                cart = Cart.objects.get(cart_id=_cart_id(request))
                cart_items = CartItem.objects.filter(cart=cart, is_active=True)
            except Cart.DoesNotExist:
                cart_items = []

        if not cart_items:
            messages.error(request, "Your cart is empty!")
            return redirect('store')

        total = Decimal('0.00')
        for item in cart_items:
            total += (item.product.price * item.quantity)
        
        tax = (Decimal('0.02') * total).quantize(Decimal('0.01'))
        shipping = Decimal('0.00') if total >= Decimal('200.00') else Decimal('15.00')
        grand_total = total + tax + shipping

        # Create Order
        order = Order()
        if request.user.is_authenticated:
            order.user = request.user
        
        order.full_name = request.POST.get('full_name')
        order.email = request.POST.get('email')
        order.phone = request.POST.get('phone')
        order.address = request.POST.get('address')
        order.city = request.POST.get('city')
        order.postal_code = request.POST.get('postal_code')
        order.country = request.POST.get('country', 'United States')
        order.order_note = request.POST.get('order_note', '')
        order.total_amount = grand_total
        order.tax = tax
        order.shipping_cost = shipping
        order.payment_method = request.POST.get('payment_method', 'Credit Card')
        order.is_paid = True
        order.status = 'Completed'

        yr = int(datetime.date.today().strftime('%Y'))
        dt = int(datetime.date.today().strftime('%d'))
        mt = int(datetime.date.today().strftime('%m'))
        d = datetime.date(yr, mt, dt)
        current_date = d.strftime("%Y%m%d")
        random_code = str(uuid.uuid4().hex[:6]).upper()
        order.order_number = f"ORD-{current_date}-{random_code}"
        order.transaction_id = f"TXN-{uuid.uuid4().hex[:10].upper()}"
        order.save()

        for item in cart_items:
            order_item = OrderItem()
            order_item.order = order
            order_item.product = item.product
            order_item.quantity = item.quantity
            order_item.price = item.product.price
            order_item.save()

            product = item.product
            product.stock -= item.quantity
            product.save()

        cart_items.delete()

        messages.success(request, "Your order has been placed successfully!")
        return redirect('order_complete', order_number=order.order_number)

    return redirect('checkout')


def order_complete(request, order_number):
    try:
        order = Order.objects.get(order_number=order_number)
        order_items = OrderItem.objects.filter(order=order)
        subtotal = sum(item.price * item.quantity for item in order_items)

        context = {
            'order': order,
            'order_items': order_items,
            'subtotal': subtotal,
        }
        return render(request, 'store/order_complete.html', context)
    except Order.DoesNotExist:
        messages.error(request, "Order not found.")
        return redirect('store')


def register(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        first_name = request.POST.get('first_name', '').strip()
        last_name = request.POST.get('last_name', '').strip()
        username = request.POST.get('username', '').strip()
        email = request.POST.get('email', '').strip()
        password = request.POST.get('password', '')
        confirm_password = request.POST.get('confirm_password', '')

        if password != confirm_password:
            messages.error(request, "Passwords do not match!")
            return render(request, 'store/register.html')

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already taken!")
            return render(request, 'store/register.html')

        if User.objects.filter(email=email).exists():
            messages.error(request, "Email address already registered!")
            return render(request, 'store/register.html')

        user = User.objects.create_user(
            username=username,
            email=email,
            password=password,
            first_name=first_name,
            last_name=last_name
        )
        user.save()

        user = authenticate(username=username, password=password)
        if user is not None:
            login(request, user)
            
            try:
                session_cart = Cart.objects.get(cart_id=_cart_id(request))
                session_cart_items = CartItem.objects.filter(cart=session_cart)
                for s_item in session_cart_items:
                    u_item, created = CartItem.objects.get_or_create(user=user, product=s_item.product)
                    if not created:
                        u_item.quantity += s_item.quantity
                        u_item.save()
                    s_item.delete()
            except Cart.DoesNotExist:
                pass

            messages.success(request, f"Welcome to Antigravity Store, {user.first_name or user.username}!")
            return redirect('dashboard')

    return render(request, 'store/register.html')


def user_login(request):
    if request.user.is_authenticated:
        return redirect('dashboard')

    if request.method == 'POST':
        username_or_email = request.POST.get('username', '').strip()
        password = request.POST.get('password', '')

        user = authenticate(username=username_or_email, password=password)
        if user is None and '@' in username_or_email:
            try:
                user_obj = User.objects.get(email=username_or_email)
                user = authenticate(username=user_obj.username, password=password)
            except User.DoesNotExist:
                user = None

        if user is not None:
            login(request, user)
            
            try:
                session_cart = Cart.objects.get(cart_id=_cart_id(request))
                session_cart_items = CartItem.objects.filter(cart=session_cart)
                for s_item in session_cart_items:
                    u_item, created = CartItem.objects.get_or_create(user=user, product=s_item.product)
                    if not created:
                        u_item.quantity += s_item.quantity
                        u_item.save()
                    s_item.delete()
            except Cart.DoesNotExist:
                pass

            messages.success(request, f"Logged in successfully as {user.username}!")
            next_url = request.GET.get('next')
            if next_url:
                return redirect(next_url)
            return redirect('dashboard')
        else:
            messages.error(request, "Invalid username or password.")

    return render(request, 'store/login.html')


def user_logout(request):
    logout(request)
    messages.info(request, "You have been logged out.")
    return redirect('store')


@login_required(login_url='login')
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    orders_count = orders.count()
    context = {
        'orders': orders,
        'orders_count': orders_count,
    }
    return render(request, 'store/dashboard.html', context)


@login_required(login_url='login')
def order_detail(request, order_number):
    order = get_object_or_404(Order, order_number=order_number, user=request.user)
    order_items = OrderItem.objects.filter(order=order)
    subtotal = sum(item.price * item.quantity for item in order_items)

    context = {
        'order': order,
        'order_items': order_items,
        'subtotal': subtotal,
    }
    return render(request, 'store/order_detail.html', context)


def submit_review(request, product_id):
    if request.method == 'POST':
        try:
            reviews = ProductReview.objects.get(user__id=request.user.id, product__id=product_id)
            subject = request.POST.get('subject', '')
            review = request.POST.get('review', '')
            rating = int(request.POST.get('rating', 5))
            reviews.subject = subject
            reviews.comment = review
            reviews.rating = rating
            reviews.save()
            messages.success(request, "Thank you! Your review has been updated.")
        except ProductReview.DoesNotExist:
            subject = request.POST.get('subject', '')
            review = request.POST.get('review', '')
            rating = int(request.POST.get('rating', 5))
            product = Product.objects.get(id=product_id)
            ProductReview.objects.create(
                user=request.user,
                product=product,
                subject=subject,
                comment=review,
                rating=rating
            )
            messages.success(request, "Thank you! Your review has been submitted.")

    return redirect(request.META.get('HTTP_REFERER'))
