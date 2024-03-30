import datetime
import random
import string
import jwt
from rest_framework.response import Response
from RestronovaRMS import settings
from rest_framework import status
from django.core.mail import EmailMessage
from .models import User

def create_response(success, message, body=None, status_code=status.HTTP_200_OK):
        response_data = {'success': success, 'message': message}
        if body is not None:
            response_data['body'] = body
        return Response(response_data, status=status_code)

from rest_framework_simplejwt.tokens import RefreshToken

def jwt_encode_handler(user):
    """Generates a JWT access token with a set expiration time."""
    refresh = RefreshToken.for_user(user)
    return {
        'access': str(refresh.access_token),
        'refresh': str(refresh)
        }

def jwt_decode_handler(token):
    """Decodes a JWT token and returns the payload."""
    return jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])

def generate_code():
    return ''.join(random.choices(string.digits, k=6))

def get_user(email):
    try:
        return User.objects.get(email=email)
    except User.DoesNotExist:
        return None

def send_verification_email(user):
    verification_code = ''.join(random.choices(string.digits, k=6))
    user.verification_code = verification_code
    user.save()
    subject = "User Registration Verification"
    message = f"Your verification code is: {verification_code}"
    email = EmailMessage(subject, message, to=[user.email])
    email.send()

def send_reset_email(email, reset_token):
    subject = "Password Reset"
    message = f"Use the following token to reset your password: {reset_token}"
    email = EmailMessage(subject, message, to=[email])
    email.send()