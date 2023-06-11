from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework.filters import SearchFilter
from rest_framework.pagination import LimitOffsetPagination
from rest_framework.viewsets import ModelViewSet

from api.filters import FilterTitles
from api.mixins import GenericMixinsSet
from api.serializers import (
    CategorySerializer, CommentSerializer, GenreSerializer,
    GetTitleSerializer, ReviewSerializer, TitleSerializer
)

from reviews.models import Category, Comment, Genre, Review, Title
from users.permissions import IsAdminOrReadPermission


class CategoryViewSet(GenericMixinsSet):
    """Вьюсет для Categories."""
    queryset = Category.objects.all()
    serializer_class = CategorySerializer
    pagination_class = LimitOffsetPagination
    permission_classes = (
        IsAdminOrReadPermission,
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
        IsAdminOrReadPermission,
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
        IsAdminOrReadPermission,
    )
    queryset = Title.objects.all()

    def get_serializer_class(self):
        if self.request.method in ('POST', 'PATCH'):
            return TitleSerializer
        return GetTitleSerializer


class ReviewViewSet(ModelViewSet):
    """Вьюсет для Reviews."""
    serializer_class = ReviewSerializer

    def get_title(self):
        """Возвращает объект текущего произведения."""
        title_id = self.kwargs.get('title_id')
        return get_object_or_404(Title, pk=title_id)

    def get_queryset(self):
        return self.get_title().reviews.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, title=self.get_title())


class CommentViewSet(ModelViewSet):
    """Вьюсет для Comments."""
    serializer_class = CommentSerializer

    def get_review(self):
        """Возвращает объект текущего отзыва."""
        review_id = self.kwargs.get('review_id')
        return get_object_or_404(Review, pk=review_id)

    def get_queryset(self):
        return self.get_review().comments.all()

    def perform_create(self, serializer):
        serializer.save(author=self.request.user, review=self.get_review())
