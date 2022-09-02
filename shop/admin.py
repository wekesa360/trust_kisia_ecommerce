from django.contrib import admin
from .models import (
    Product,
    OrderItem,
    Order,
    Category,
    DeliveryCharges,
    Customer,
    ProductImage
)

admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(Category)
admin.site.register(DeliveryCharges)
admin.site.register(Customer)

class PictureInline(admin.StackedInline):
    model = ProductImage
    
class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline]
    
admin.site.register(Product, ProductAdmin)