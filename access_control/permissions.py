from rest_framework.permissions import BasePermission
from rest_framework.exceptions import PermissionDenied, NotAuthenticated
from .services import check_permission


METHOD_ACTION_MAP = {
    "GET": "read",
    "POST": "create",
    "PUT": "update",
    "PATCH": "update",
    "DELETE": "delete",
}


class RBACPermission(BasePermission):

    def has_permission(self, request, view):

        if not request.user:
            raise NotAuthenticated("Authentication credentials were not provided.")

        resource = getattr(view, "resource_name", None)

        if not resource:
            return True  # если ресурс не указан — не ограничиваем

        action = METHOD_ACTION_MAP.get(request.method)

        if not check_permission(request.user, resource, action):
            raise PermissionDenied("You do not have permission for this action.")

        return True