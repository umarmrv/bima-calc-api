from django.utils import timezone
from rest_framework import serializers
from .models import Quote, Application, Tariff, CarType
from .utils import (
    BASE_PRICES, AGE_RANGES, EXP_RANGES, CAR_COEF,
    pick_from_ranges, RULESET_VERSION, QUOTE_TTL_DAYS, Calculated
)
from datetime import timedelta


class QuoteCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = ("id", "tariff", "driver_age", "driver_experience", "car_type")
        read_only_fields = ("id",)

    def validate(self, data):
        age = data["driver_age"]
        exp = data["driver_experience"]
        if not (18 <= age <= 100):
            raise serializers.ValidationError({"driver_age": "18..100"})
        if not (0 <= exp <= 80):
            raise serializers.ValidationError({"driver_experience": "0..80"})
        if exp > age - 18:
            raise serializers.ValidationError({"driver_experience": "не может быть > age-18"})
        return data

    def create(self, validated):
        user = self.context["request"].user
        # расчёт
        base = float(BASE_PRICES[validated["tariff"]])
        c_age = pick_from_ranges(validated["driver_age"], AGE_RANGES)
        c_exp = pick_from_ranges(validated["driver_experience"], EXP_RANGES)
        c_car = float(CAR_COEF[validated["car_type"]])
        total = round(base * c_age * c_exp * c_car, 2)

        return Quote.objects.create(
            user=user,
            **validated,
            base_amount=base,
            coef_age=c_age,
            coef_exp=c_exp,
            coef_car=c_car,
            total_amount=total,
            currency="TJS",
            ruleset_version=RULESET_VERSION,
            valid_until=timezone.now() + timedelta(days=QUOTE_TTL_DAYS),
            status=Quote.Status.ACTIVE,
        )


class QuoteDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Quote
        fields = (
            "id", "tariff", "driver_age", "driver_experience", "car_type",
            "base_amount", "coef_age", "coef_exp", "coef_car",
            "total_amount", "currency", "ruleset_version",
            "valid_until", "status", "created_at",
        )


class ApplicationCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Application
        fields = ("id", "full_name", "phone", "email", "tariff", "quote")
        read_only_fields = ("id",)

    def validate(self, data):
        quote = data["quote"]
        user = self.context["request"].user
        if quote.user_id != user.id:
            raise serializers.ValidationError({"quote": "чужой расчёт"})
        if quote.status != Quote.Status.ACTIVE:
            raise serializers.ValidationError({"quote": f"недопустимый статус {quote.status}"})
        if quote.valid_until <= timezone.now():
            raise serializers.ValidationError({"quote": "просрочен"})
        return data

    def create(self, validated):
        user = self.context["request"].user
        quote = validated["quote"]

        app = Application.objects.create(
            user=user,
            quote=quote,
            full_name=validated["full_name"],
            phone=validated["phone"],
            email=validated["email"],
            tariff=validated["tariff"],
            total_amount_snapshot=quote.total_amount,
        )
        quote.status = Quote.Status.USED
        quote.save(update_fields=["status"])
        return app


class ApplicationDetailSerializer(serializers.ModelSerializer):
    user = serializers.StringRelatedField()
    class Meta:
        model = Application
        read_only_fields = fields = (
            "id", "user", "quote", "full_name", "phone", "email", "tariff",
            "total_amount_snapshot", "status", "meta", "created_at", "updated_at"
        )
