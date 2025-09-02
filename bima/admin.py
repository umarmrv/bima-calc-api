# core/admin.py
from django.contrib import admin
from .models import Quote, Application

@admin.register(Quote)
class QuoteAdmin(admin.ModelAdmin):
    list_display = ("id","user","tariff","total_amount","status","valid_until","created_at")
    list_filter = ("tariff","status","created_at")

@admin.register(Application)
class ApplicationAdmin(admin.ModelAdmin):
    list_display = ("id","user","tariff","total_amount_snapshot","status","created_at")
    list_filter = ("tariff","status","created_at")
