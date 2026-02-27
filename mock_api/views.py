from rest_framework.views import APIView
from rest_framework.response import Response
from access_control.permissions import RBACPermission


class OrdersView(APIView):
    permission_classes = [RBACPermission]
    resource_name = "orders"

    def get(self, request):
        return Response([
            {"id": 1, "name": "Order 1"},
            {"id": 2, "name": "Order 2"},
        ])

    def post(self, request):
        return Response({"message": "Order created"})