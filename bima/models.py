import uuid
from datetime import timedelta
from django.conf import settings
from django.db import models
from django.utils import timezone


class Tariff(models.TextChoices):
    OSAGO = "OSAGO", "OSAGO"
    KASKO = "KASKO", "KASKO"


class CarType(models.TextChoices):
    SEDAN = "sedan", "Sedan"
    SUV = "suv", "SUV"
    TRUCK = "truck", "Truck"
    SPORT = "sport", "Sport"


class Quote(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "ACTIVE"
        USED = "USED"
        EXPIRED = "EXPIRED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="quotes")

    tariff = models.CharField(max_length=20, choices=Tariff.choices)
    driver_age = models.PositiveSmallIntegerField()
    driver_experience = models.PositiveSmallIntegerField()
    car_type = models.CharField(max_length=20, choices=CarType.choices)

    base_amount = models.DecimalField(max_digits=12, decimal_places=2)
    coef_age = models.DecimalField(max_digits=6, decimal_places=3)
    coef_exp = models.DecimalField(max_digits=6, decimal_places=3)
    coef_car = models.DecimalField(max_digits=6, decimal_places=3)
    total_amount = models.DecimalField(max_digits=12, decimal_places=2)
    currency = models.CharField(max_length=3, default="TJS")
    ruleset_version = models.CharField(max_length=16, default="v1")

    valid_until = models.DateTimeField()
    status = models.CharField(max_length=10, choices=Status.choices, default=Status.ACTIVE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.id} {self.tariff} {self.total_amount} {self.currency}"


class Application(models.Model):
    class Status(models.TextChoices):
        NEW = "NEW"
        IN_REVIEW = "IN_REVIEW"
        APPROVED = "APPROVED"
        REJECTED = "REJECTED"
        CANCELLED = "CANCELLED"
        EXPIRED = "EXPIRED"

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="applications")
    quote = models.OneToOneField(Quote, on_delete=models.PROTECT, related_name="application")

    full_name = models.CharField(max_length=100)
    phone = models.CharField(max_length=32)
    email = models.EmailField()
    tariff = models.CharField(max_length=20, choices=Tariff.choices)
    total_amount_snapshot = models.DecimalField(max_digits=12, decimal_places=2)

    status = models.CharField(max_length=12, choices=Status.choices, default=Status.NEW)
    meta = models.JSONField(default=dict, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.id} {self.tariff} {self.total_amount_snapshot} {self.status}"
