from django.urls import path
from .views import (RegisterView, UserDetailsView)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('get-details', UserDetailsView.as_view(), name='get-details'),
]