from django.db.models.signals import post_save
import uuid
from .models import Customer, ProcessOrder, CancelledOrder
from django.shortcuts import get_object_or_404
from .functions import send_confirm_order_email, send_cancel_order_email, get_total_charges
from django.dispatch import receiver
import logging

logger = logging.getLogger(__name__)

@receiver(post_save, sender=ProcessOrder)
def handle_new_order(sender, instance, created, **kwargs):
    if created:
        order = ProcessOrder.objects.get(id=instance.id)
        if order.cancel_order == False:
            send_confirm_order_email(order)
            order.total_charges = get_total_charges(order)[1]
            order.save()
        else:
            print(order.order.uuid + "  :order cancelled")

@receiver(post_save, sender=CancelledOrder)
def handle_new_order(sender, instance, created, **kwargs):
    if created:
        cancelled_order = CancelledOrder.objects.get(id=instance.id)
        if cancelled_order.order_cancelled == True:
            send_cancel_order_email(cancelled_order)
        else:
            print(cancelled_order.order_id + "  :order not cancelled")
        


 