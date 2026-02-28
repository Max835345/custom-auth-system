from access_control.models import UserRole, RolePermission, Permission

def check_permission(user, resource_name: str, action: str) -> bool:
    if not user:
        return False

    user_roles = UserRole.objects.filter(user=user).select_related("role")

    role_ids = [ur.role.id for ur in user_roles]

    permissions = Permission.objects.filter(
        resource__name=resource_name,
        action=action
    )

    if not permissions.exists():
        return False

    permission_ids = [p.id for p in permissions]

    has_permission = RolePermission.objects.filter(
        role_id__in=role_ids,
        permission_id__in=permission_ids
    ).exists()

    return has_permission
