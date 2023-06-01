from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views

router_v1 = DefaultRouter()

router_v1.register()
router_v1.register()
router_v1.register()

urlpatterns = [
    path('v1/', include(router_v1.urls)),
]
