from apps.users.models import User

def update_user_provider():
    users = User.objects.all()
    for user in users:
        user.provider = "credentials"
        user.save()

update_user_provider()

# run type folder\filename.py | python manage.py shell command to run the scripts