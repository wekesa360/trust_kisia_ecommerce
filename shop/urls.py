from django.urls import path
from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    category_products_view,
    category_view,
    checkout_view,
    order_summary_view

)

app_name = 'retail'

urlpatterns = [
    path('', category_view, name='home'),
    path('product<pk>/',category_products_view, name='product'),
    path('order-summary/', order_summary_view, name='order-summary'),
    path('checkout/', checkout_view, name='checkout'),
    path('add-to-cart/<pk>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<pk>', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<pk>/', reduce_quantity_item, name='reduce-quantity-item')
    
]