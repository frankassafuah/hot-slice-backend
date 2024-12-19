from django.shortcuts import render
from rest_framework.generics import CreateAPIView, GenericAPIView, RetrieveAPIView
from authentication.serializers import RegisterSerializer, LoginSerializer
from django.contrib.auth import authenticate
from rest_framework import response, status, permissions
from rest_framework_simplejwt.tokens import RefreshToken
from authentication.models import User
import logging


# Create your views here.

logger = logging.getLogger(__name__)


class RegisterAPIView(CreateAPIView):
    authentication_classes = []
    serializer_class = RegisterSerializer

    def perform_create(self, serializer):
        instance = serializer.save()
        instance.set_password(instance.password)
        instance.save()


class LoginAPIView(GenericAPIView):
    authentication_classes = []
    serializer_class = LoginSerializer

    def post(self, request):
        email = request.data.get("email", None)
        password = request.data.get("password", None)

        user = authenticate(username=email, password=password)
        print(f"user {user}")

        if user is not None:
            serializer = self.serializer_class(user)
            token = self.get_tokens_for_user(user)
            return response.Response(
                {"message": "Login successful", "data": serializer.data, "access_token": token},
                status=status.HTTP_201_CREATED,
            )
        return response.Response(
            {"message": "Invalid credentials, try again"},
            status=status.HTTP_401_UNAUTHORIZED,
        )

    def get_tokens_for_user(self, user):
        refresh = RefreshToken.for_user(user)

        return {
            "refresh": str(refresh),
            "access": str(refresh.access_token),
        }


class AuthUserAPIView(GenericAPIView):
    permission_classes = [permissions.IsAuthenticated]
    serializer_class = RegisterSerializer

    def get(self, request):
        user = request.user
        serializer = self.serializer_class(user)
        return response.Response({"user": serializer.data})