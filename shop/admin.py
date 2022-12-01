from django.contrib import admin
from .models import (
    Product,
    OrderItem,
    Order,
    Category,
    DeliveryCharges,
    Customer,
    ProductImage,
    ProcessOrder,
    CancelledOrder,
    EmailDispatch
)
@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('customer', 'status', 'ordered_date', 'ordered')
@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('product', 'quantity', 'ordered', 'customer')
@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('category_name', 'sub_category', 'type')
@admin.register(DeliveryCharges)
class DeliveryCharges(admin.ModelAdmin):
    list_display = ('county', 'specific_location', 'fee')
@admin.register(Customer)
class CustomerAdmin(admin.ModelAdmin):
    list_display = ('first_name','device', 'phone_number', 'email', 'ordered')
@admin.register(ProcessOrder)
class ProcessOrderAdmin(admin.ModelAdmin):
    list_display = ('order', 'total_charges', 'payment_transacted', 'cancel_order')
class PictureInline(admin.TabularInline):
    model = ProductImage
    
@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [PictureInline]
    list_display = ('name', 'quantity', 'brand', 'price', 'tag', 'category')

@admin.register(CancelledOrder)
class CancelledOrderAdmin(admin.ModelAdmin):
    list_display = ('customer_name', 'customer_email', 'order_id', 'products_order', 'order_cancelled')

@admin.register(EmailDispatch)
class EmailDispatchAdmin(admin.ModelAdmin):
    list_display = ('name', 'email', 'subject')