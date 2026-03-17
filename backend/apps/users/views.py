from apps.users.models import User
from datetime import timedelta
from utils.validators import validate_post_request_with_fields
from django.http import HttpRequest, JsonResponse
from django.contrib.auth.hashers import check_password, make_password
from django.views.decorators.csrf import csrf_exempt
from django.utils import timezone
from dotenv import dotenv_values
import json
import uuid
import jwt


def _encode_token(user_id: int) -> str:
    return jwt.encode(
        payload={
            'user_id': user_id,
            'exp': timezone.now() + timedelta(days=1),
            'iat': timezone.now(),
            'jti': str(uuid.uuid4()),
        },
        key=dotenv_values()["JWT_SECRET_KEY"],
        algorithm='HS256'
    )


@ csrf_exempt
@ validate_post_request_with_fields(["username", "email", "password"])
def register(request: HttpRequest) -> JsonResponse:
    body_params = json.loads(request.body.decode('utf-8'))
    username = body_params["username"]
    email = body_params["email"]

    if User.objects.filter(email=email).exists():
        return JsonResponse({'status': 400, 'message': 'Invalid pre-existing email.'})

    password = body_params["password"]
    hashed_password = make_password(password)

    user = User.objects.create(
        username=username,
        email=email,
        password=hashed_password
    )
    user.save()

    token = _encode_token(user.id)

    return JsonResponse({'message': 'User created successfully.', 'token': token}, status=201)


@ csrf_exempt
@ validate_post_request_with_fields(["email", "password"])
def login(request: HttpRequest):
    body_params = json.loads(request.body.decode('utf-8'))
    email = body_params["email"]
    password = body_params["password"]

    user = User.objects.filter(email=email).first()
    if not user:
        return JsonResponse({'message': 'Invalid email or password.'}, status=400)

    if check_password(password, user.password):
        token = _encode_token(user.id)
        return JsonResponse({'message': 'Login successful.', 'token': token, 'username': user.username}, status=200)
    else:
        return JsonResponse({'message': 'Invalid email or password.'}, status=400)


@csrf_exempt
def reset_chat_history(request: HttpRequest):
    user_id = request.user_id
    user = User.objects.get(id=user_id)
    user.chat_history = []
    user.save()

    return JsonResponse({'message': 'Chat history reset successfully.'}, status=200)


@csrf_exempt
def get_chat_history(request: HttpRequest):
    user_id = request.user_id
    user = User.objects.get(id=user_id)
    return JsonResponse({'chat_history': user.chat_history}, status=200)
