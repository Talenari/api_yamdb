from django.core.mail import send_mail
from django.shortcuts import get_object_or_404
from django.contrib.auth.tokens import default_token_generator
from rest_framework import permissions, status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.filters import SearchFilter
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework_simplejwt.tokens import RefreshToken


from django.conf import settings
from users.models import User
from users.pagination import UserPagination
from users.permissions import AdminPermission
from users.serializers import (UserSerializer,
                               UserSignupSerializer,
                               UserTokenSerializer)


class UserModelViewSet(ModelViewSet):
    """Просмотр и изменение профиля пользователей администратором."""
    queryset = User.objects.all()
    serializer_class = UserSerializer
    lookup_field = 'username'
    pagination_class = UserPagination
    permission_classes = (AdminPermission,)
    filter_backends = (SearchFilter,)
    search_fields = ('username',)
    http_method_names = ['get', 'post', 'delete', 'patch']


class UserMeModelView(APIView):
    """Просмотр и патч своего профиля пользователем."""
    permission_classes = (permissions.IsAuthenticated,)

    def get(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(user)
        return Response(serializer.data)

    def patch(self, request):
        user = get_object_or_404(User, username=request.user.username)
        serializer = UserSerializer(
            user,
            context={'request': request},
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data)


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def usergettoken(request):
    serializer = UserTokenSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    user = get_object_or_404(
        User,
        username=serializer.validated_data.get('username')
    )
    if default_token_generator.check_token(
        serializer.validated_data.get('confirmation_code')
    ):
        token = RefreshToken.for_user(user)
        return Response(
            {'access': str(token.access_token)},
            status=status.HTTP_200_OK
        )


@api_view(['POST'])
@permission_classes([permissions.AllowAny])
def usersignup(request):
    serializer = UserSignupSerializer(data=request.data)
    serializer.is_valid(raise_exception=True)
    try:
        user, _ = User.objects.get_or_create(
            username=request.data['username'],
            email=request.data['email']
        )
    except Exception:
        return Response(
            {'data': 'Данные username или email недоступны'},
            status=status.HTTP_400_BAD_REQUEST
        )
    user.confirmation_code = default_token_generator.make_token(user)
    send_mail(
        'Ваш код подтверждения',
        f'Ваш код подтверждения {user.confirmation_code}.',
        settings.MAIL,
        [f'{user.email}'],
    )
    return Response(serializer.data, status=status.HTTP_200_OK)
