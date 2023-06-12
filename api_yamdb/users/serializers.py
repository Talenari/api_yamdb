from re import match

from rest_framework.serializers import ModelSerializer
from rest_framework.validators import ValidationError
from rest_framework.serializers import CharField, EmailField

from users.models import User


class UserSignupSerializer(ModelSerializer):
    """Сериализатор создания пользователя."""
    username = CharField()
    email = EmailField()

    class Meta:
        model = User
        fields = ['username', 'email']

    def validate_username(self, value):
        if len(value) > 150:
            raise ValidationError('username больше 254 символов')
        if not match(r'^[\w.@+-]+\Z', value):
            raise ValidationError('username введен неверно')
        if value == 'me':
            raise ValidationError('"me" в "username" недопустимо')
        return value

    def validate_email(self, value):
        if len(value) > 254:
            raise ValidationError('email больше 254 символов')
        return value


class UserTokenSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = [
            'username',
            'confirmation_code'
        ]


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
        if not self.context['request'].user.is_admin:
            raise ValidationError
        return value
