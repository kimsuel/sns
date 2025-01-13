from rest_framework import serializers

from api.features.models import Post, Image, Comment, Like, Follow, Bookmark


class ImageSerializer(serializers.ModelSerializer):

    class Meta:
        model = Image
        fields = ['id', 'image']


class PostSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, required=False)

    class Meta:
        model = Post
        fields = ['text', 'user', 'images']

    def create(self, validated_data):
        user = validated_data.get('user')
        images = self.context['request'].FILES.getlist('images')
        post = Post.objects.create(**validated_data)

        for image in images:
            img_instance = Image.objects.create(image=image, user=user)
            post.image.add(img_instance)

        return post


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    class Meta:
        model = Follow
        fields = '__all__'


class BookmarkSerializer(serializers.ModelSerializer):
    class Meta:
        model = Bookmark
        fields = '__all__'
