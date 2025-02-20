from django.db import models
from django.contrib.auth import get_user_model
import uuid

User = get_user_model()

class GemWallet(models.Model):
    STATE_CHOICES = [
        ('ACTIVE', 'Active'),
        ('SUSPENDED', 'Suspended'),
        ('CLOSED', 'Closed'),
    ]
    STATUS_CHOICES = [
        ('PENDING', 'Pending'),
        ('APPROVED', 'Approved'),
        ('DECLINED', 'Declined'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='wallet')
    balance = models.DecimalField(max_digits=20, decimal_places=2, default=0.00)
    state = models.CharField(max_length=20, choices=STATE_CHOICES, default='ACTIVE')
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='APPROVED')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Wallet"

    def credit(self, amount):
        """Add gems to wallet balance."""
        self.balance += amount
        self.save()

    def debit(self, amount):
        """Deduct gems from wallet balance if sufficient funds are available."""
        if self.balance >= amount:
            self.balance -= amount
            self.save()
        else:
            raise ValueError("Insufficient balance")
