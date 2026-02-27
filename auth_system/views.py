from rest_framework.views import APIView
from rest_framework.response import Response
from users.models import User
from access_control.models import Role, UserRole
from .utils import hash_password, check_password
from .jwt_utils import generate_token
from .jwt_utils import decode_token


class RegisterView(APIView):
    def post(self, request):

        first_name = request.data.get("first_name")
        last_name = request.data.get("last_name")
        middle_name = request.data.get("middle_name")
        email = request.data.get("email")
        password = request.data.get("password")
        password_repeat = request.data.get("password_repeat")

        if not all([first_name, last_name, email, password, password_repeat]):
            return Response({"error": "Missing required fields"}, status=400)

        if password != password_repeat:
            return Response({"error": "Passwords do not match"}, status=400)

        if User.objects.filter(email=email).exists():
            return Response({"error": "User already exists"}, status=400)

        user = User.objects.create(
            first_name=first_name,
            last_name=last_name,
            middle_name=middle_name,
            email=email,
            password_hash=hash_password(password),
        )


        return Response({"message": "User created"}, status=201)

class LoginView(APIView):

    def post(self, request):
        email = request.data["email"]
        password = request.data["password"]

        try:
            user = User.objects.get(email=email)
        except User.DoesNotExist:
            return Response({"error": "Invalid credentials"}, status=401)

        if user.is_deleted:
            return Response({"error": "Account deleted"}, status=401)

        if not check_password(password, user.password_hash):
            return Response({"error": "Invalid credentials"}, status=401)

        token = generate_token(user)

        return Response({"access_token": token})


class LogoutView(APIView):
    def post(self, request):
        return Response({"message": "Logged out"})

class UpdateUserView(APIView):

    def put(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return Response({"error": "Unauthorized"}, status=401)

        token = token.split(" ")[1]
        payload = decode_token(token)

        user = User.objects.get(id=payload["user_id"])

        user.first_name = request.data.get("first_name", user.first_name)
        user.last_name = request.data.get("last_name", user.last_name)
        user.middle_name = request.data.get("middle_name", user.middle_name)

        user.save()

        return Response({"message": "User updated"})

class DeleteUserView(APIView):

    def delete(self, request):
        token = request.headers.get("Authorization")

        if not token:
            return Response({"error": "Unauthorized"}, status=401)

        token = token.split(" ")[1]
        payload = decode_token(token)

        user = User.objects.get(id=payload["user_id"])
        user.is_deleted = True
        user.save()

        return Response({"message": "Account deleted"})