from rest_framework.views import APIView
from rest_framework.response import Response
from access_control.models import Role, Permission, RolePermission
from access_control.permissions import RBACPermission
from auth_system.jwt_utils import decode_token
from users.models import User


class CreateRoleView(APIView):
    permission_classes = [RBACPermission]
    resource_name = "roles"

    def post(self, request):
        role = Role.objects.create(
            name=request.data["name"],
            description=request.data.get("description", "")
        )
        return Response({"id": role.id, "name": role.name})


class AssignPermissionToRoleView(APIView):
    permission_classes = [RBACPermission]
    resource_name = "roles"

    def post(self, request):
        role = Role.objects.get(id=request.data["role_id"])
        permission = Permission.objects.get(id=request.data["permission_id"])

        RolePermission.objects.create(role=role, permission=permission)

        return Response({"message": "Permission assigned"})

class AddPermissionToRoleView(APIView):

    def post(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return Response({"error": "Unauthorized"}, status=401)

        token = token.split(" ")[1]
        payload = decode_token(token)
        user = User.objects.get(id=payload["user_id"])

        if not user.userrole_set.filter(role__name="ADMIN").exists():
            return Response({"error": "Forbidden"}, status=403)

        role = Role.objects.get(name=request.data["role"])
        permission = Permission.objects.get(id=request.data["permission_id"])

        RolePermission.objects.create(role=role, permission=permission)

        return Response({"message": "Permission added"})