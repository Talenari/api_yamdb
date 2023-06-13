from django.urls import include, path
from rest_framework.routers import SimpleRouter

from users.views import (UserMeModelView,
                         UserModelViewSet,
                         usersignup,
                         usergettoken)


router_users_v1 = SimpleRouter()
router_users_v1.register('users', UserModelViewSet)

auth_patterns = [
    path('signup/', usersignup),
    path('token/', usergettoken),
]

urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('users/me/', UserMeModelView.as_view()),
    path('', include(router_users_v1.urls)),
]
