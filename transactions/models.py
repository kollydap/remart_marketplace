from django.db import models
import uuid
from django.contrib.auth import get_user_model
from gemwallets.models import GemWallet
from orders.models import Order
from django.utils.crypto import get_random_string

User = get_user_model()


class TransactionState(models.TextChoices):
    PENDING = "pending", "Pending"
    ACCEPTED = "accepted", "Accepted"
    ESCROWED = "escrowed", "Escrowed"
    SHIPPED = "shipped", "Shipped"
    COMPLETED = "completed", "Completed"
    DISPUTED = "disputed", "Disputed"
    CANCELLED = "cancelled", "Cancelled"
    REFUNDED = "refunded", "Refunded"
    RELEASE_FAILED = "release_failed", "Release Failed"
    REFUND_FAILED = "refund_failed", "Refund Failed"


class TransactionStatus(models.TextChoices):
    PROCESSING = "processing", "Processing"
    SUCCESS = "success", "Success"
    FAILED = "failed", "Failed"


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order = models.OneToOneField(
        Order, on_delete=models.CASCADE, related_name="transaction"
    )
    sender = models.ForeignKey(
        GemWallet, on_delete=models.CASCADE, related_name="sent_transactions"
    )
    receiver = models.ForeignKey(
        GemWallet, on_delete=models.CASCADE, related_name="received_transactions"
    )
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    state = models.CharField(
        max_length=20,
        choices=TransactionState.choices,
        default=TransactionState.PENDING,
        editable=False,
    )
    status = models.CharField(
        max_length=20,
        choices=TransactionStatus.choices,
        default=TransactionStatus.PROCESSING,
    )
    signature = models.CharField(max_length=64, unique=True, editable=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def save(self, *args, **kwargs):
        if not self.signature:
            self.signature = get_random_string(64)
        super().save(*args, **kwargs)

    def __str__(self):
        return f"Transaction {self.id} for Order {self.order.id} - {self.amount} Gems ({self.state})"

    class Meta:
        ordering = ["-created_at"]
