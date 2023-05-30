from django.core.mail import send_mail
from rest_framework.serializers import ModelSerializer

from .models import User


class UserSignupSerializer(ModelSerializer):
    class Meta:
        model = User
        fields = ['username', 'email']

    def create(self, validated_data):
        password = User.objects.make_random_password(length=32)
        send_mail(
            'Код подтверждения',
            f'Ваш код подтверждения {password}.',
            'from@example.com',
            ['to@example.com'],
        )
        return User.objects.create(
            username=validated_data.get('username'),
            email=validated_data.get('email'),
            password=password
        )
