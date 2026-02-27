import jwt
import datetime
from django.conf import settings

SECRET_KEY = "super_secret_key"

def generate_token(user):
    payload = {
        "user_id": str(user.id),
        "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
    }

    return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

def decode_token(token):
    return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])