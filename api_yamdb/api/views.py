from django.shortcuts import render

from reviews.models import Category, Genre, Title
from .serializers import (
    CategorySerializer, GenreSerializer, TitleSerializer
)
