from django.db import models
from django.contrib.auth.models import AbstractUser
import uuid
from django.contrib.auth import get_user_model


class CustomUser(AbstractUser):
    id = models.UUIDField(
        primary_key=True, default=uuid.uuid4, editable=False
    )  # UUID as primary key
    email = models.EmailField(unique=True)

    GENDER_CHOICES = [
        ("M", "Male"),
        ("F", "Female"),
        ("O", "Other"),
    ]

    gender = models.CharField(max_length=1, choices=GENDER_CHOICES, blank=True)
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    profile_picture = models.CharField(max_length=500)
    device = models.CharField(max_length=250)
    is_email_verified = models.BooleanField(default=False)
    is_phone_verified = models.BooleanField(default=False)
    last_login_ip = models.GenericIPAddressField(null=True, blank=True)
    referral_code = models.CharField(max_length=20, unique=True, null=True, blank=True)
    loyalty_points = models.IntegerField(default=0)
    last_purchase_date = models.DateTimeField(null=True, blank=True)
    registration_ip = models.GenericIPAddressField(null=True, blank=True)
    gdpr_consent = models.BooleanField(default=False)
    online_status = models.CharField(
        max_length=20,
        choices=[
            ("ONLINE", "Online"),
            ("OFFLINE", "Offline"),
        ],
        default="ONLINE",
    )
    account_status = models.CharField(
        max_length=20,
        choices=[
            ("ACTIVE", "Active"),
            ("SUSPENDED", "Suspended"),
            ("BANNED", "Banned"),
        ],
        default="ACTIVE",
    )

    def __str__(self):
        return self.username


User = get_user_model()


class SuspiciousActivity(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    previous_ip = models.GenericIPAddressField()
    new_ip = models.GenericIPAddressField()
    timestamp = models.DateTimeField(auto_now_add=True)
    action = models.CharField(max_length=100)
    device_info = models.TextField(null=True)
    is_resolved = models.BooleanField(default=False)
    resolution_notes = models.TextField(null=True)

    class Meta:
        ordering = ["-timestamp"]


class Address(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="addresses")
    street = models.CharField(max_length=255)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=100)
    postal_code = models.CharField(max_length=20)
    country = models.CharField(max_length=100)
    latitude = models.FloatField()
    longitude = models.FloatField()
    is_primary = models.BooleanField(default=False)  # To mark the default address

    def save(self, *args, **kwargs):
        # If this address is set as primary, unset all other primary addresses for this user
        if self.is_primary:
            Address.objects.filter(user=self.user, is_primary=True).update(
                is_primary=False
            )
        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.street}, {self.city}, {self.country}"
