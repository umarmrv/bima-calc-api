from django.shortcuts import render
from rest_framework import mixins, viewsets
from rest_framework.permissions import IsAuthenticated
#
from drf_spectacular.utils import extend_schema
from rest_framework import permissions, status , generics
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Quote, Application
from .serializer import (
    QuoteCreateSerializer, QuoteDetailSerializer,
    ApplicationCreateSerializer, ApplicationDetailSerializer,
    RegisterSerializer, RegisterResponseSerializer
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

@extend_schema(auth=[], tags=["auth"])
class RegisterView(generics.CreateAPIView):
    permission_classes = [permissions.AllowAny]
    serializer_class = RegisterSerializer

    @extend_schema(
        request=RegisterSerializer,
        responses={201: RegisterResponseSerializer},
    )
    def post(self, request, *args, **kwargs):
        # оставляем кастомный ответ с токенами
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = serializer.save()
        refresh = RefreshToken.for_user(user)
        return Response({
            "id": user.id,
            "username": user.get_username(),
            "email": user.email,
            "access": str(refresh.access_token),
            "refresh": str(refresh),
        }, status=status.HTTP_201_CREATED)