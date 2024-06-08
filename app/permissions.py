
from rest_framework.exceptions import PermissionDenied
from rest_framework.permissions import BasePermission

from app import choices, models

class HasUserPermission(BasePermission):
    message = "You are not authorized to perform this action."
    obj_message = "Only creator is allowed to perform this action."

    def has_permission(self, request, view):
        if request.user.role in [choices.UserRole.ADMIN, choices.UserRole.MANAGER]:
            return True
        raise PermissionDenied(detail={"errors": {"non_field_errors": [self.message]}})

    def has_object_permission(self, request, view, obj):
        print(request.user , obj.owner)
        if request.user == obj.owner or request.user == obj:
            return True
        raise PermissionDenied(
            detail={"errors": {"non_field_errors": [self.obj_message]}}
        )
