import environ
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
env = environ.Env()
environ.Env.read_env()

def is_production():
     return env('ENVIRONMENT') == "PRODUCTION"

class CookieJWTAuthentication(JWTAuthentication):

    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None

        try:
            validated_token = self.get_validated_token(token)
            user = self.get_user(validated_token)
            return (user, validated_token)
        except Exception:
            raise AuthenticationFailed("Invalid token")
