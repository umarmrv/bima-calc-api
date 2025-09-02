from rest_framework.permissions import BasePermission

class IsOwner(BasePermission):
    def has_object_permission(self, request, view, obj):
        user_id = getattr(obj, "user_id", None)
        return bool(request.user and request.user.is_authenticated and user_id == request.user.id)
