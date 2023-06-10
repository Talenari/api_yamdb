from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import (UserMeModelView,
                         UserModelViewSet,
                         UserSignupView,
                         UserTokenView)


router_users_v1 = SimpleRouter()
router_users_v1.register('users', UserModelViewSet)

urlpatterns = [
    path('auth/signup/', UserSignupView.as_view()),
    path('auth/token/', UserTokenView.as_view()),
    path('users/me/', UserMeModelView.as_view()),
    path('', include(router_users_v1.urls)),
]
