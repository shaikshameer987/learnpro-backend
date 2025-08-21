from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
from utils.response import success_response, failure_response, get_strutured_error, set_cookie
from .serializers import UserSerializer, RegisterSerializer
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
from utils.response import CustomApiView
from common.constants import CREDENTIALS, PROVIDER_CHOICES
from apps.users.models import User, UserSocialProfile

# Create your views here.

class RegisterView(CustomApiView):
    permission_classes = [AllowAny]

    def post(self, request):
        serializer = RegisterSerializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            user_data = UserSerializer(user).data
            response = success_response(user_data, status.HTTP_201_CREATED)
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)
            response = set_cookie(response,token=access_token )
            return response

        errors = serializer.errors
        first_error = get_strutured_error(errors=errors, request_data=request.data)

        return failure_response(first_error["message"], first_error["error_code"], status.HTTP_400_BAD_REQUEST)


class UserDetailsView(CustomApiView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        accessToken = request.COOKIES.get('access_token')
        token = AccessToken(accessToken)
        user = User.objects.get(id=token["user_id"])
        serializer = UserSerializer(user)
        return success_response(serializer.data)

class LoginView(CustomApiView):
    permission_classes = [AllowAny]

    def post(self, request):
        email = request.data.get("email")
        provider = request.data.get("provider")
        password = request.data.get("password")

        if not email or not provider:
            msg = "Email and Provider are required"
            return failure_response(msg, "REQUIRED", status.HTTP_400_BAD_REQUEST)

        if(provider == CREDENTIALS):
            print("here1")
            if not password:
                msg = "Password is required"
                return failure_response(msg, "REQUIRED", status.HTTP_400_BAD_REQUEST)

            user = User.objects.filter(email=email).first()

            if not user:
                msg = "User does not exist with this email"
                return failure_response(msg, "INVALID_EMAIL", status.HTTP_400_BAD_REQUEST)

            if user.check_password(password):
                serializer = UserSerializer(user)
                response = success_response(serializer.data, status.HTTP_201_CREATED)
                refresh = RefreshToken.for_user(user)
                access_token = str(refresh.access_token)
                response = set_cookie(response,token=access_token)
                return response

            else:
                msg = "Password is incorrect"
                return failure_response(msg, "INVALID_PASSWORD", status.HTTP_400_BAD_REQUEST)

        if not any(provider == choice[0] for choice in PROVIDER_CHOICES):
            msg = "Invalid provider"
            return failure_response(msg, "INVALID_PROVIDER", status.HTTP_400_BAD_REQUEST)

        user = User.objects.filter(email=email).first()

        user_social_profile = UserSocialProfile.objects.filter(user=user,provider=provider).first()

        if not user or not user_social_profile:
            msg = "User does not exist with this email"
            return failure_response(msg, "INVALID_EMAIL", status.HTTP_400_BAD_REQUEST)

        serializer = UserSerializer(user)
        response = success_response(serializer.data, status.HTTP_201_CREATED)
        refresh = RefreshToken.for_user(user)
        access_token = str(refresh.access_token)
        response = set_cookie(response,token=access_token)
        return response