import jwt
from datetime import datetime, timedelta
from django.conf import settings
from ninja.security import HttpBearer
from django.shortcuts import get_object_or_404
from ninja.errors import HttpError
from .models import User

# 1. Fungsi Pembuat Token (Access & Refresh)
def create_tokens(user_id: int):
    access_exp = datetime.utcnow() + timedelta(hours=1)
    refresh_exp = datetime.utcnow() + timedelta(days=7)
    access_token = jwt.encode({"user_id": user_id, "type": "access", "exp": access_exp}, settings.SECRET_KEY, algorithm="HS256")
    refresh_token = jwt.encode({"user_id": user_id, "type": "refresh", "exp": refresh_exp}, settings.SECRET_KEY, algorithm="HS256")
    return {"access_token": access_token, "refresh_token": refresh_token}

# 2. Middleware Verifikasi Token
class JWTAuth(HttpBearer):
    def authenticate(self, request, token):
        try:
            payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
            if payload.get("type") != "access":
                return None
            user = get_object_or_404(User, id=payload["user_id"])
            request.user = user
            return token
        except jwt.ExpiredSignatureError:
            raise HttpError(401, "Token kedaluwarsa")
        except jwt.InvalidTokenError:
            raise HttpError(401, "Token tidak valid")

# 3. Role-Based Access Control (RBAC) Decorators
def check_role(request, allowed_roles):
    if not hasattr(request, 'user') or request.user.role not in allowed_roles:
        raise HttpError(403, "Akses ditolak: Anda tidak memiliki privilege (Role) yang sesuai.")

def is_admin(request):
    check_role(request, ['admin'])

def is_instructor(request):
    check_role(request, ['instructor', 'admin'])

def is_student(request):
    check_role(request, ['student', 'admin'])