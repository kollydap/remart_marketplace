from django.contrib.auth.signals import user_logged_in
from django.contrib.auth import get_user_model
from django.dispatch import receiver
from ipware import get_client_ip

User = get_user_model()


@receiver(user_logged_in, sender=User)
def update_last_login_ip(sender, instance, request, **kwargs):
    if request:
        client_ip, is_routable = get_client_ip(request)
        instance.last_login_ip = client_ip
        instance.save()
