from rest_framework.views import APIView
from rest_framework.permissions import AllowAny
from rest_framework import status
from apps.users.models import User
from utils.response import (success_response, failure_response, get_strutured_error)
from utils.helpers import (is_production)
from .serializers import RegisterUserSerializer
from rest_framework_simplejwt.tokens import RefreshToken


# Create your views here.

class RegisterView(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = success_response(RegisterUserSerializer(user).data, status.HTTP_201_CREATED)
            production = is_production()

            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            response.set_cookie(
                key="access_token",
                value=access_token,
                httponly=True,
                max_age=7 * 24 * 60 * 60,
                secure=production,
                samesite="Strict" if production else "Lax",
            )

            return response

        errors = serializer.errors
        first_error = get_strutured_error(errors=errors, request_data=request.data)

        return failure_response(first_error["message"], first_error["error_code"], status.HTTP_400_BAD_REQUEST)

    def http_method_not_allowed(self, request):
        msg= f"{request.method} method is not allowed"
        return failure_response(msg, "METHOD_NOT_ALLOWED", status.HTTP_405_METHOD_NOT_ALLOWED)