from django.db.models.signals import post_save
from .models import Order, ProcessOrder, DeliveryCharges, OrderItem
from django.shortcuts import get_object_or_404
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ProcessOrder)
def handle_new_order(sender, instance, created, **kwargs):
    print('signal>>>>>>>>>>>>>>>',created)
    print(kwargs.get('updated'), '<<<<<<<<<<<<<<<<signal')
    if created:
        order = ProcessOrder.objects.get(id=instance.id)
        if order.cancel_order == False:
            order_items = OrderItem.objects.filter(customer=order.order.customer)
            first_name = order.order.customer.first_name
            order_id = order.order.customer.first_name
            print(order.order.uuid, order_items)


 