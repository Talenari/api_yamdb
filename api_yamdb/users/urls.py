from django.urls import path

from .views import UserSignupView, UserGetTokenView


urlpatterns = [
    path('auth/signup/', UserSignupView.as_view()),
    path('auth/token/', UserGetTokenView),
]
