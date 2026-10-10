from django.urls import path
from . import views

urlpatterns = [
    path('', views.store, name='store'),
    path('category/<slug:category_slug>/', views.store, name='products_by_category'),
    path('category/<slug:category_slug>/<slug:product_slug>/', views.product_detail, name='product_detail'),
    path('search/', views.search, name='search'),
    
    # Cart routes
    path('cart/', views.cart, name='cart'),
    path('cart/add/<int:product_id>/', views.add_cart, name='add_cart'),
    path('cart/decrement/<int:product_id>/<int:cart_item_id>/', views.remove_cart, name='remove_cart'),
    path('cart/remove/<int:product_id>/<int:cart_item_id>/', views.remove_cart_item, name='remove_cart_item'),
    
    # Checkout & Orders
    path('checkout/', views.checkout, name='checkout'),
    path('place-order/', views.place_order, name='place_order'),
    path('order-complete/<str:order_number>/', views.order_complete, name='order_complete'),
    
    # User Auth & Dashboard
    path('register/', views.register, name='register'),
    path('login/', views.user_login, name='login'),
    path('logout/', views.user_logout, name='logout'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('order-detail/<str:order_number>/', views.order_detail, name='order_detail'),
    
    # Reviews
    path('submit-review/<int:product_id>/', views.submit_review, name='submit_review'),
]
