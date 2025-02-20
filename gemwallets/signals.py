from django.db.models.signals import post_save
from django.dispatch import receiver
from django.conf import settings
from gemwallets.models import GemWallet


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_wallet(sender, instance, created, **kwargs):
    if created:
        GemWallet.objects.create(user=instance)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def save_user_wallet(sender, instance, **kwargs):
    instance.wallet.save()
