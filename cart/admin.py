from django.contrib import admin

from .models import Product, Cart, CartProduct, OrdersItem, OrdersPerformed

# Register your models here.

admin.site.register(Product)
admin.site.register(Cart)
admin.site.register(CartProduct)
admin.site.register(OrdersItem)
admin.site.register(OrdersPerformed)