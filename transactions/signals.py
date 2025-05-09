from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from transactions.models import Transaction
from orders.models import Order


@receiver(post_save, sender=Order)
def initiate_transaction(sender, instance, created, **kwargs):
    if created:
        Transaction.objects.create(
            order=instance,
            sender=instance.buyer.wallet,
            amount=instance.total_gems,
            receiver=instance.product.owner.wallet,
        )


@receiver(post_save, sender=Order)
def save_user_wallet(sender, instance, **kwargs):
    instance.transaction.save()
