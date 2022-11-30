from django.db.models.signals import post_save
from .models import Order, ProcessOrder, DeliveryCharges, OrderItem
from django.shortcuts import get_object_or_404
from .functions import send_confirm_order_email
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ProcessOrder)
def handle_new_order(sender, instance, created, **kwargs):
    if created:
        order = ProcessOrder.objects.get(id=instance.id)
        if order.cancel_order == False:
            send_confirm_order_email(order)
        else:
            print(order.order.uuid + "  :order cancelled")

            


 