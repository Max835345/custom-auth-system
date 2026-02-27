from users.models import User
from .jwt_utils import decode_token
from django.http import JsonResponse

class JWTAuthenticationMiddleware:

    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):

        auth_header = request.headers.get("Authorization")

        if auth_header and auth_header.startswith("Bearer "):
            token = auth_header.split(" ")[1]
            try:
                payload = decode_token(token)
                user = User.objects.get(id=payload["user_id"], is_active=True, is_deleted=False)
                request.user = user
            except:
                request.user = None
        else:
            request.user = None

        return self.get_response(request)