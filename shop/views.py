from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist 
from django.utils import timezone
import datetime
from django.http import HttpResponseRedirect
from django.urls import reverse
from .models import (
    Category,
    Product,
    ProductImage,
    DeliveryCharges,
    OrderItem,
    Order,
    Customer
)


def category_view(request):
    """The home view where
    every product is separated in to their categories

    Args:
        request (_type_): _description_

    Returns:
        _type_: _description_
    """
    if request.method == 'GET':
        products = Product.objects.all()
    return render(request, 'product.html', context={'products': products})    

def category_products_view(request, slug):
    """products rendered based on category.

    Args:
        request (_type_): _description_
        slug (_type_): _description_
    """
    try:
        if request.method == 'POST':
            category = Category.objects.get(slug='slug')
            products = Product.object.all().filter(category=category)
            
            return render(request, 'product.html', context= {'products': products})
    except ObjectDoesNotExist:
        return redirect('shop:home')

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    order_qs = Order.objects.filter(
        
    )
            
