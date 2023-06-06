from rest_framework.mixins import (
    CreateModelMixin, DestroyModelMixin, ListModelMixin
)
from rest_framework.viewsets import GenericViewSet


class GenericMixinsSet(GenericViewSet,
                       CreateModelMixin,
                       DestroyModelMixin,
                       ListModelMixin):
    """Создание, чтение, запись."""
    pass
