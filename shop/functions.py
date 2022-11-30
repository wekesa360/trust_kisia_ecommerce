from django.utils import timezone
from datetime import date
from .models import DeliveryCharges, OrderItem
from django.conf import settings
from django.core.mail import send_mail as sm
from django.template.loader import render_to_string


def get_order_details(order):
    order = order.order
    customer = order.customer
    order_items = OrderItem.objects.filter(customer=customer)
    first_name = customer.first_name
    recipient_email = customer.email
    delivery_location = customer.delivery_address
    order_id = order.uuid
    order_id = str(order_id)
    return [first_name, order_id, order_items, delivery_location, recipient_email]

def get_total_charges(order):
    total = 0
    details = get_order_details(order)
    items = details[2]
    specific_location = details[-2]
    # delivery_location = DeliveryCharges.objects.get(specific_location=specific_location)
    location_charges = specific_location.fee
    for item in items:
        total += item.get_final_price()
    total_charges = location_charges + total
    return [location_charges, total_charges]

def send_confirm_order_email(order):
    details = get_order_details(order)
    recipient_list = [details[-1]]
    total_charges = get_total_charges(order)
    msg_html = render_to_string('email/order.html', {'first_name': details[0],
                                                            'order_id': details[1],
                                                            'total_charges': total_charges[1],
                                                            'delivery_location':details[-2],
                                                            'delivery_charges': total_charges[0],
                                                            'products': details[2]})
    res = sm(
        subject = 'Trust Kisia Ecommerce: Your Order',
        message = '',
        from_email = settings.EMAIL_HOST_USER,
        recipient_list = recipient_list,
        html_message=msg_html,
        fail_silently=False,
    )
    print(f"Email sent to {res} members")
    
    
