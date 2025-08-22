import environ
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, AuthenticationFailed
import boto3
import mimetypes

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


def upload_to_s3(file, path):
    bucket_name = env("S3_BUCKET_NAME")
    bucket_region = env('S3_REGION')
    s3 = boto3.client(
        "s3",
        aws_access_key_id=env('S3_ACCESS_KEY'),
        aws_secret_access_key=env('S3_SECRET_KEY'),
        region_name=bucket_region,
    )

    content_type, _ = mimetypes.guess_type(path)
    if content_type is None:
        content_type = 'application/octet-stream'  # fallback

    print(content_type)

    s3.upload_fileobj(Fileobj=file, Bucket=bucket_name, Key=path,  ExtraArgs={'ContentType': content_type})

    return f"https://{bucket_name}.s3.{bucket_region}.amazonaws.com/{path}"