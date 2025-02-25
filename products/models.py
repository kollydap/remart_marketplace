from django.db import models
import uuid
from django.contrib.auth import get_user_model
from django.utils import timezone
from datetime import timedelta


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
    image = models.CharField(max_length=500)
    category = models.ForeignKey(
        ProductCategory, on_delete=models.CASCADE, related_name="products"
    )
    owner = models.ForeignKey(User, on_delete=models.CASCADE, related_name="products")
    location = models.CharField(max_length=255)  # Location of the product
    # location = models.ForeignKey(
    #     Address, on_delete=models.CASCADE, related_name="products"
    # )
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

    def save(self, *args, **kwargs):
        # Call the parent class's save() method first
        super().save(*args, **kwargs)

        # Get products with high views in the last 7 days
        one_week_ago = timezone.now() - timedelta(days=7)
        high_views = Product.objects.filter(
            views__gte=100,  # Adjust the threshold as needed
            created_at__gte=one_week_ago,
            is_active=True,
        )

        # Get new arrivals added in the last 3 days
        new_arrivals = Product.objects.filter(
            created_at__gte=timezone.now() - timedelta(days=3), is_active=True
        )

        # Combine and update as featured
        featured_products = high_views | new_arrivals
        featured_products.update(is_featured=True)


class ProductView(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    product = models.ForeignKey(
        Product, on_delete=models.CASCADE, related_name="product_views"
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ("product", "user")  # Ensure one view per user

    def __str__(self):
        return f"{self.user.username} viewed {self.product.name}"


# class ProductAddress(models.Model):
#     product = models.OneToOneField(
#         Product, on_delete=models.CASCADE, related_name="address"
#     )
#     street = models.CharField(max_length=255)
#     city = models.CharField(max_length=100)
#     state = models.CharField(max_length=100)
#     postal_code = models.CharField(max_length=20)
#     country = models.CharField(max_length=100)
#     latitude = models.FloatField()
#     longitude = models.FloatField()

#     def __str__(self):
#         return f"{self.street}, {self.city}, {self.country}"


# Location: Indicates where the product is located, useful for local pickups or delivery.
# Quantity: For products with more than one unit available.
# Is Active: To mark products as sold or unavailable without deleting them.
# Is Featured: For promoting certain products on the homepage or special sections.
# Views: To track how many times a product has been viewed.
