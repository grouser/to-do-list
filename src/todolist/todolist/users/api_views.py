from django.contrib import auth
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from .api_serializers import LoginSerializer


class LoginAPIView(APIView):
    serializer_class = LoginSerializer
    permission_classes = []

    def post(self, request, format=None):
        user_serializer = self.serializer_class(data=request.data)
        if user_serializer.is_valid():
            request.user = user_serializer.instance
            auth.login(request, request.user)
            return Response('')
        return Response(user_serializer.errors, status=status.HTTP_401_UNAUTHORIZED)


class LogoutAPIView(APIView):
    permission_classes = []

    def get(self, request, format=None):
        auth.logout(request)
        return Response('')