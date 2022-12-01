from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
import uuid as unique_gen
import json
from django.core.exceptions import ObjectDoesNotExist 
from django.utils import timezone
from django.core import serializers
from django.http import HttpResponse
from .forms import CheckoutForm
from .models import (
    Category,
    Product,
    OrderItem,
    Order,
    Customer,
    ProcessOrder,
    DeliveryCharges,
    CancelledOrder
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
        try:
            product_items = Product.objects.all()
        except ObjectDoesNotExist:
            print("Object does not exist")
        return render(request, 'index.html', context={'products': product_items})    

def product_view(request, slug):
    product = get_object_or_404(Product, slug=slug)
    return render(request, 'product-details.html', context= {'product': product})

def search_view(request):
    qs = Product.objects.all()
    response = serializers.serialize('json', qs)
    return HttpResponse(response, content_type='application/json') 

def category_products_view(request, slug):
    """products rendered based on category.

    Args:
        request (_type_): _description_
        slug (_type_): _description_
    """
    try:
        if request.method == 'GET':
            category = Category.objects.get(slug=slug)
            products = Product.objects.all().filter(category=category)
            return render(request, 'product.html', context= {'products': products})
    except ObjectDoesNotExist:
        return redirect('shop:home')

def add_to_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    device = request.COOKIES['device']
    customer = Customer.objects.get_or_create(device=device)
    customer= get_object_or_404(Customer, device=device)
    order_item, created = OrderItem.objects.get_or_create(
        product=product,
        customer=customer,
        ordered=False,
    )
    order_qs = Order.objects.filter(customer=customer, ordered=False)
    product = Product.objects.get(slug=slug)
    if product.quantity > 0:
        if order_qs.exists():
            order = order_qs[0]
            if order.products.filter(product__pk=product.pk).exists():
                product.quantity -= 1
                product.save()
                if product.quantity > 0:
                    order_item.quantity += 1
                    order_item.save()
                else:
                    messages.error(request, 'Product out of stock')
                    return redirect('shop:order-summary')
                messages.info(request, 'Added quantity item')
                return redirect('shop:order-summary')
            else:
                order.products.add(order_item)
                messages.info(request, 'Item added to your cart')
                return redirect('shop:order-summary')   
        else:
            ordered_date = timezone.now()
            try:
                order = Order.objects.get(customer=customer, ordered_date=ordered_date)
            except ObjectDoesNotExist:
                uuid = unique_gen.uuid4()
                order = Order.objects.create(customer=customer, ordered_date=ordered_date, uuid=uuid)
            order.products.add(order_item)
            product.quantity -= 1
            product.save()
            messages.info(request,'Item added to your cart')
            return redirect('shop:order-summary')
    else:
        messages.error(request, 'Product out of stock')
        return redirect('shop:order-summary')
 
def order_summary_view(request):
    try:
        device = request.COOKIES['device']
        customer = Customer.objects.get_or_create(device=device)
        customer= get_object_or_404(Customer, device=device)
        order = Order.objects.get(customer=customer, ordered=False)
        context = {
            'object': order
        }
        return render(request, 'cart.html', context)
    except ObjectDoesNotExist:
        messages.error(request, 'You do not have an order')
        return redirect('/')

def persists_view(request):
    """Serialize publications from Publicaiton model to JSON format

    Args:
        request

    Returns:
        HttpResponse: response( JSON format)
    """
    try: 
        device=request.COOKIES['device']
        qs = Customer.objects.get(device=device)
        ordered = Order.objects.get(customer__device=device)
        if qs:
            if qs.email == None and ordered.ordered != True:
                qs = {'value':False}
            else:
                qs = {'value':True}
    except ObjectDoesNotExist:
        qs = {'value':False}
    qs = json.dumps(qs)
    response = qs
    return HttpResponse(response, content_type='application/json')

def remove_from_cart(request, slug):
    product = get_object_or_404(Product, slug=slug)
    device = request.COOKIES['device']
    customer = Customer.objects.get_or_create(device=device)
    customer= get_object_or_404(Customer, device=device)
    order_qs = Order.objects.filter(
        customer=customer,
        ordered=False
    )
    if order_qs.exists():
        order = order_qs[0]
        if order.products.filter(product__pk=product.pk).exists():
            order_item = OrderItem.objects.filter(
                product= product,
                customer__device= customer.device,
                ordered = False
            )[0]
            order_item.delete()
            # Supposed to be a cron job or signal --- all quanatity 
            product = get_object_or_404(Product, slug=slug)
            product.quantity = product.quantity + order_item.quantity
            product.save()
            messages.info(request, 'Item \"'+order_item.product.name+'\" removed from cart')
            return redirect('shop:order-summary')
        else:
            messages.info(request, 'This item is not in your cart')
            return redirect('shop:product', slug=slug)
    else:
        messages.info(request, 'You do not have an order')
        return redirect('shop:product', slug=slug)

def reduce_quantity_item(request, slug):
    product = get_object_or_404(Product, slug=slug)
    device = request.COOKIES['device']
    customer = Customer.objects.get_or_create(device=device)
    customer= get_object_or_404(Customer, device=device)
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
            if order_item.quantity > 1 :
                order_item.quantity -= 1
                order_item.save()
                product = Product.objects.get(slug=slug)
                product.quantity += 1
                product.save()
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
        customer= get_object_or_404(Customer, device=device)
        order = Order.objects.get(customer=customer, ordered=False)
        context = {
            'form': form,
            'object': order
        }
        return render(request, 'checkout.html', context)
    if request.method == 'POST':
        device = request.COOKIES['device']
        customer = Customer.objects.get_or_create(device=device)
        customer = get_object_or_404(Customer, device=device, )
        form = CheckoutForm(request.POST or None)
        if form.is_valid():
            if customer.email != form.cleaned_data.get('email_address'):
                customer.first_name = form.cleaned_data.get('first_name')
                customer.last_name = form.cleaned_data.get('last_name')
                customer.phone_number = form.cleaned_data.get('phone_number') 
                customer.email = form.cleaned_data.get('email_address')
                customer.delivery_address = form.cleaned_data.get('delivery_address')
                customer.ordered = True
                customer.save()
        else:
            messages.info(request, 'cannot save details')
            return redirect('shop:checkout')
        if customer.ordered == True:
            order = get_object_or_404(Order, customer=customer, ordered=False)
            order.ordered = True
            order.uuid=unique_gen.uuid4()
            order.save()
            if order.ordered == True:
                ordered_item = OrderItem.objects.filter(customer=order.customer, ordered=False)
                for item in ordered_item:
                    item.ordered = True
                    item.save()
                ProcessOrder.objects.create(
                    order=order,
                )
        return render(request, 'success.html')

def cancel_order_view(request,  order_id):
    order_id = unique_gen.UUID(order_id)
    if request.method == 'GET':
        process_order = get_object_or_404(ProcessOrder,order__uuid=order_id)
        if process_order:
            process_order.cancel_order = True
            process_order.save()
        if process_order.cancel_order == True:
            cancelled_order = CancelledOrder()
            customer = process_order.order.customer
            cancelled_order.customer_name = f'{customer.first_name} {customer.last_name}'
            cancelled_order.customer_email = customer.email
            cancelled_order.order_cancelled = True
            cancelled_order.order_id = str(order_id)
            products = []
            for product_order_item in process_order.order.products.all():
                products.append(product_order_item.product)
                # Supposed to be a cron job or signal --- all quanatity 
                p_product = get_object_or_404(Product, slug=product_order_item.product.slug)
                p_product.quantity =   p_product.quantity + product_order_item.quantity
                p_product.save()
                print(product_order_item.quantity)
            cancelled_order.products_order = products
            cancelled_order.save()
            customer_device = customer.device
            customer_record = Customer.objects.get(device=customer_device)
            customer_record.delete()
        else:
            messages.error(request,'Order does not exist! ')
            return render(request, 'success-order-cancel.html')
        messages.info(request,'Order Cancelled')
        return render(request, 'success-order-cancel.html')
    else:
        return render(request, 'success-order-cancel.html')
