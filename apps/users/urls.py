from django.urls import path
from .views import (RegisterView, UserDetailsView, LoginView)

urlpatterns = [
    path('register', RegisterView.as_view(), name='register'),
    path('get-details', UserDetailsView.as_view(), name='get-details'),
    path('login', LoginView.as_view(), name='login'),
]