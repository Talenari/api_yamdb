from rest_framework.serializers import ModelSerializer

from users.models import User


class UserSignupSerializer(ModelSerializer):
    """Сериализатор создания пользователя."""
    class Meta:
        model = User
        fields = ['username', 'email']


class UserSerializer(ModelSerializer):
    """Сериализатор просмотра пользователя админом."""
    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'bio',
            'first_name',
            'last_name',
            'role'
        ]


class UserMeSerializer(ModelSerializer):
    """Сериализатор просмотра своего профиля пользователем."""

    class Meta:
        model = User
        fields = [
            'username',
            'email',
            'bio',
            'first_name',
            'last_name',
            'role'
        ]
        read_only_fields = ['role']
