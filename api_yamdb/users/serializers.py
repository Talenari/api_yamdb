from django.contrib.auth.hashers import make_password
from django.core.mail import send_mail
from rest_framework.serializers import ModelSerializer

from rest_framework.validators import ValidationError

from users.models import User


class UserSignupSerializer(ModelSerializer):
    """Сериализатор создания пользователя."""
    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        password = User.objects.make_random_password(length=32)
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения {password}.',
            'from@example.com',
            [f'{validated_data.get("email")}'],
        )
        return User.objects.get_or_create(
            username=self.data.get('username'),
            email=self.data.get('email'),
            password=make_password(password)
        )


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
