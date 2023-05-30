from rest_framework.generics import CreateAPIView

from .models import User
from .serializers import UserSignupSerializer


class UserSignupView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSignupSerializer
