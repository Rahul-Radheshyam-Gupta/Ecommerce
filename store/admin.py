from django.contrib import admin

# Register your models here.
from .models import Customer,Product,ShippingAddress,Order,OrderItem

admin.site.register(Customer)
admin.site.register(Product)
admin.site.register(ShippingAddress)
admin.site.register(Order)
admin.site.register(OrderItem)
