from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import permissions
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from api.filters import FilterTitles
from api.mixins import GenericMixinsSet
from api.serializers import (
    CategorySerializer, GenreSerializer, GetTitleSerializer, TitleSerializer
)
from api.permissions import AdminPermissions
from reviews.models import Category, Genre, Title


class CategoryViewSet(GenericMixinsSet):
    """Вьюсет для Categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminPermissions, permissions.IsAuthenticatedOrReadOnly,
    )
    lookup_field = 'slug'
    search_fields = ('name', )
    filter_backends = (SearchFilter,)


class GenreViewSet(GenericMixinsSet):
    """Вьюсет для Genres."""
    queryset = Genre.objects.all()
    serializer_class = GenreSerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminPermissions, permissions.IsAuthenticatedOrReadOnly,
    )
    lookup_field = 'slug'
    search_fields = ('name', )
    filter_backends = (SearchFilter,)


class TitleViewSet(ModelViewSet):
    """Вьюсет для Titles."""
    filterset_class = FilterTitles
    filter_backends = (DjangoFilterBackend,)
    pagination_class = LimitOffsetPagination
    permission_classes = (
        AdminPermissions, permissions.IsAuthenticatedOrReadOnly,
    )
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return GetTitleSerializer
