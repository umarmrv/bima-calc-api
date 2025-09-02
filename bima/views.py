from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Quote, Application
from .serializer import (
    QuoteCreateSerializer, QuoteDetailSerializer,
    ApplicationCreateSerializer, ApplicationDetailSerializer
)

class QuoteViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Quote.objects.filter(user=self.request.user).order_by("-created_at")
    def get_serializer_class(self):
        return QuoteCreateSerializer if self.action == "create" else QuoteDetailSerializer

class ApplicationViewSet(mixins.CreateModelMixin, mixins.RetrieveModelMixin, mixins.ListModelMixin, viewsets.GenericViewSet):
    permission_classes = [IsAuthenticated]
    def get_queryset(self):
        return Application.objects.filter(user=self.request.user).order_by("-created_at")
    def get_serializer_class(self):
        return ApplicationCreateSerializer if self.action == "create" else ApplicationDetailSerializer
