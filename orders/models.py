from django.db import models
import uuid
from django.contrib.auth import get_user_model
from gemwallets.models import GemWallet
from products.models import Product

User = get_user_model()


class OrderStatus(models.TextChoices):
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


class Order(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="orders")
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="orders"
    )
    quantity = models.PositiveIntegerField(default=1)
    total_gems = models.PositiveIntegerField()
    state = models.CharField(
        max_length=20,
        choices=OrderStatus.choices,
        default=OrderStatus.PENDING,
    )
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Order {self.id} - {self.product.name} by {self.buyer.username}"

    class Meta:
        ordering = ["-created_at"]
