from rest_framework.permissions import (AllowAny, IsAuthenticated)
from rest_framework import status
from apps.users.models import User
from utils.response import (success_response, failure_response, get_strutured_error, set_cookie)
from .serializers import (RegisterUserSerializer, LoginUserSerializer)
from rest_framework_simplejwt.tokens import (RefreshToken, AccessToken)
from utils.response import CustomApiView


# Create your views here.

class RegisterView(CustomApiView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterUserSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            response = success_response(serializer.data, status.HTTP_201_CREATED)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = set_cookie(response,token=access_token )
            return response

        errors = serializer.errors
        first_error = get_strutured_error(errors=errors, request_data=request.data)

        return failure_response(first_error["message"], first_error["error_code"], status.HTTP_400_BAD_REQUEST)


class UserDetailsView(CustomApiView):
    permission_classes = [IsAuthenticated]
    serializer_class = RegisterUserSerializer

    def get(self, request):
        accessToken = request.COOKIES.get('access_token')
        token = AccessToken(accessToken)
        user = User.objects.get(id=token["user_id"])
        serializer = self.serializer_class(user)
        return success_response(serializer.data)

class LoginView(CustomApiView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = LoginUserSerializer(data=request.data)
        if serializer.is_valid():
            return success_response(serializer.data, status.HTTP_200_OK)

        errors = serializer.errors
        first_error = get_strutured_error(errors=errors, request_data=request.data)

        return failure_response(first_error["message"], first_error["error_code"], status.HTTP_400_BAD_REQUEST)