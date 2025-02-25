from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from notifications.models import Notification
from orders.models import Order


@receiver(post_save, sender=Order)
def create_notification(sender, instance, created, **kwargs):
    print("yooooo")
    if created:
        Notification.objects.create(
            user=instance.product.owner,
            message=f"🎉 {instance.buyer.username} just ordered {instance.quantity}x {instance.product.name}! Ready to roll? 🚀"
            # link=instance.link,
        )
