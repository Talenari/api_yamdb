from rest_framework import serializers

from reviews.models import Review, Comments


class ReviewSerializer(serializers.ModelSerializer):
    pass


class CommentSerializer(serializers.ModelSerializer):
    pass
