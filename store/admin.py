from django.contrib import admin
from .models import Category, Product, Cart, CartItem, Order, OrderItem, ProductReview

class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    prepopulated_fields = {'slug': ('name',)}

class ProductAdmin(admin.ModelAdmin):
    list_display = ('name', 'price', 'stock', 'category', 'updated_at', 'is_available', 'featured')
    prepopulated_fields = {'slug': ('name',)}
    list_filter = ('category', 'is_available', 'featured')
    list_editable = ('price', 'stock', 'is_available', 'featured')
    search_fields = ('name', 'description')

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('product', 'quantity', 'price')

class OrderAdmin(admin.ModelAdmin):
    list_display = ('order_number', 'full_name', 'email', 'phone', 'total_amount', 'status', 'is_paid', 'created_at')
    list_filter = ('status', 'is_paid', 'created_at')
    search_fields = ('order_number', 'full_name', 'email', 'phone')
    list_editable = ('status', 'is_paid')
    inlines = [OrderItemInline]

class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'created_at')
    list_filter = ('rating', 'created_at')

admin.site.register(Category, CategoryAdmin)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart)
admin.site.register(CartItem)
admin.site.register(Order, OrderAdmin)
admin.site.register(OrderItem)
admin.site.register(ProductReview, ProductReviewAdmin)
