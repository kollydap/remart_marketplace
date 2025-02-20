from django.db import models
import uuid
from django.contrib.auth import get_user_model


User = get_user_model()


class ProductCategory(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class ProductState(models.TextChoices):
    MINT = "mint", "Mint"
    PRESTIGE = "prestige", "Prestige"
    GOOD_CONDITION = "good_condition", "Good Condition"
    FAIR = "fair", "Fair"
    NEEDS_REPAIR = "needs_repair", "Needs Repair"


class Product(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)
    description = models.TextField()
    price_in_gems = models.PositiveIntegerField()
    state = models.CharField(max_length=20, choices=ProductState.choices)
    image = models.ImageField(upload_to="product_images/", blank=True, null=True)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="products"
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    location = models.CharField(max_length=255)  # Location of the product
    quantity = models.PositiveIntegerField(default=1)
    is_premium = models.BooleanField(default=False)
    is_active = models.BooleanField(
        default=True
    )  # To indicate if the product is still available
    is_featured = models.BooleanField(default=False)  # For special promotions
    views = models.PositiveIntegerField(default=0)  # Track product views
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name


# Location: Indicates where the product is located, useful for local pickups or delivery.
# Quantity: For products with more than one unit available.
# Is Active: To mark products as sold or unavailable without deleting them.
# Is Featured: For promoting certain products on the homepage or special sections.
# Views: To track how many times a product has been viewed.
