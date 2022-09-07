from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.core.exceptions import ObjectDoesNotExist 
from django.utils import timezone

from shop.forms import CheckoutForm
from .models import (
    Category,
    Product,
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
    return render(request, 'index.html', context={'products': products})    

def category_products_view(request):
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
    device = request.COOKIES['device']
    customer = Customer.objects.get_or_create(device=device)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        customer=customer,
        ordered=False
    )
    
    order_qs = Order.objects.filter(customer=customer, ordered=False)
    
    if order_qs.exists():
        order = order_qs[0]
        
        if order.products.filter(product__pk=product.pk).exists():
            order_item.quantity += 1
            order_item.save()
            messages.info(request, 'Added quantity item')
            return redirect('shop:order-summary')
        else:
            order.products.add(order_item)
            messages.info(request, 'Item added to your cart')
            return redirect('shop:order-summary')
        
    else:
        ordered_date = timezone.now()
        order = Order.objects.create(customer=customer, ordered_date=ordered_date)
        order.products.add(order_item)
        messages.info(request,'Item added to your cart')
        return redirect('shop:order-summary')
 

def order_summary_view(request):
    try:
        device = request.COOKIES['device']
        customer = Customer.objects.get_or_create(device=device)
        order = Order.objects.get(customer__device=customer.device, ordered=False)
        context = {
            'object': order
        }
        return render(request, 'cart.html', context)
    except ObjectDoesNotExist:
        messages.error(request, 'You do not have an order')
        return redirect('/')

   
def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    device = request.COOKIES['device']
    customer = Customer.objects.get_or_create(device=device)
    order_qs = Order.objects.filter(
        customer=customer,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product= product,
                customer= customer,
                ordered = False
            )[0]
            order_item.delete()
            messages.info(request, 'Item \"'+order_item.product.name+'\" removed from cart')
            return redirect('shop:order-summary')
        else:
            messages.info(request, 'This item is not in your cart')
            return redirect('shop:product', slug=slug)
    else:
        messages.info(request, 'You do not have an order')
        return redirect('shop:product', slug=slug)

def reduce_quantity_item(request, slug):
    product = get_object_or_404(Product, slug)
    device = request.COOKIES['device']
    customer = Customer.objects.get_or_create(device=device)
    order_qs = Order.objects.filter(
        customer=customer,
        ordered = False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product=product,
                ordered=False,
                customer=customer
            )[0]
            if order_item.quantity > 1:
                order_item.quantity -= 1
                order_item.save()
            else:
                order_item.delete()
            messages.info(request, 'Product quantity was updated')
            return redirect('shop:order-summary')
        else:
            messages.info(request, 'This product is not in your cart')
            return redirect('shop:order-summary')
    else:
        messages.info(request, 'You do not have an order')
        return redirect('shop:order-summary')
    

def checkout_view(request):
    if request.method == 'GET':
        form = CheckoutForm()
        device = request.COOKIES['device']
        customer = Customer.objects.get_or_create(device=device)
        order = Order.objects.get(customer=customer, ordered=False)
        context = {
            'form': form,
            'order': order
        }
        return render(request, 'checkout.html', context)

    if request.method == 'POST':
        customer = Customer.objects.get_or_create(device=device)
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            customer.delivery_address = form.cleaned_data.get('delivery_address')
            customer.first_name = form.cleaned_data.get('first_name')
            customer.last_name = form.cleaned_data.get('last_name')
            customer.phone_number = form.cleaned_data.get('phone_number')
            customer.email = form.cleaned_data.get('emal')
            customer.save()
        
        else:
            messages.info(request, 'cannot save details')
            return redirect('shop:checkout')
        
        return render(request, 'success.html')