from .models import Category, Cart, CartItem
from .views import _cart_id

def menu_links(request):
    links = Category.objects.all()
    return dict(categories=links)

def counter(request):
    cart_count = 0
    if 'admin' in request.path:
        return {}
    try:
        if request.user.is_authenticated:
            cart_items = CartItem.objects.filter(user=request.user, is_active=True)
        else:
            cart = Cart.objects.filter(cart_id=_cart_id(request))
            cart_items = CartItem.objects.filter(cart=cart[:1], is_active=True)
        
        for cart_item in cart_items:
            cart_count += cart_item.quantity
    except Cart.DoesNotExist:
        cart_count = 0
    return dict(cart_count=cart_count)
