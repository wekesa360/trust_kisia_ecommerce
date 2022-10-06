from django.urls import path
from .views import (
    remove_from_cart,
    reduce_quantity_item,
    add_to_cart,
    category_products_view,
    category_view,
    checkout_view,
    order_summary_view,
    product_view,
    search_view

)

app_name = 'shop'

urlpatterns = [
    path('', category_view, name='home'),
    path('products/<str:slug>/',category_products_view, name='products'),
    path('product-details/<str:slug>/',product_view, name='product-details'),
    path('order-summary/', order_summary_view, name='order-summary'),
    path('checkout/', checkout_view, name='checkout'),
    path('search-product', search_view, name='search'),
    path('add-to-cart/<str:slug>/', add_to_cart, name='add-to-cart'),
    path('remove-from-cart/<str:slug>/', remove_from_cart, name='remove-from-cart'),
    path('reduce-quantity-item/<str:slug>/', reduce_quantity_item, name='reduce-quantity-item')
    
]