from rest_framework import serializers
from api.features.bookmark.models import Bookmark
from api.features.post.serializers import ImageSerializer, PostReadSerializer


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'


class SimpleBookmarkSerializer(serializers.ModelSerializer):
    post_first_image = serializers.SerializerMethodField()

    class Meta:
        model = Bookmark
        fields = ['id', 'post', 'post_first_image']

    def get_post_first_image(self, obj):
        image = obj.post.images.first()
        serializer = ImageSerializer(instance=image)
        return serializer.data


class BookmarkReadSerializer(serializers.ModelSerializer):
    post = PostReadSerializer()

    class Meta:
        model = Bookmark
        fields = ['id', 'post']
