from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError

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

    def validate_role(self, value):
        if value == self.context['request'].user.role:
            return ValidationError
        return value


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
        ]
        read_only_fields = ['username', 'email']
