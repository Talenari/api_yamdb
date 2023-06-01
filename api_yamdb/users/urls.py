from django.urls import path

from .views import UserSignupView, user_get_token


urlpatterns = [
    path('auth/signup/', UserSignupView.as_view()),
    path('auth/token/', user_get_token),
]
