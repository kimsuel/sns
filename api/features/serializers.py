import json

from rest_framework import serializers

from api.features.models import Post, Image, Comment, Like, Follow, Bookmark
from common.config import create_presigned_url
from common.kafka.producer import MessageProducer


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        if user != self.instance.user or user != self.instance.post.user:
            raise serializers.ValidationError('Only the author can edit and delete.')
        return data


class LikeReadSerializer(serializers.ModelSerializer):
    username = serializers.ReadOnlyField(source='user.username')

    class Meta:
        model = Like
        fields = ['id', 'username']


class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = '__all__'


class FollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.ReadOnlyField(source='follower.username')
    followee_name = serializers.ReadOnlyField(source='followee.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_name', 'followee', 'followee_name']


class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='followee.id')
    username = serializers.ReadOnlyField(source='followee.username')

    class Meta:
        model = Follow
        fields = ['user_id', 'username']


class FolloweeSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='follower.id')
    username = serializers.ReadOnlyField(source='follower.username')

    class Meta:
        model = Follow
        fields = ['user_id', 'username']


class SimpleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['url']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Post
        fields = ['text', 'user', 'images']
        read_only_fields = ['user']


class PostCreateSerializer(serializers.ModelSerializer):
    urls = serializers.ListSerializer(child=serializers.URLField(read_only=True), read_only=True)
    images = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Post
        fields = ['id', 'urls', 'text', 'images']
        read_only_fields = ['id']
        write_only_fields = ['text']

    def create(self, validated_data):
        user = self.context['request'].user
        images = validated_data.pop('images', [])
        validated_data['user'] = user
        post = Post.objects.create(**validated_data)

        # celery 호출
        # update_post_cache.delay(user_id=user.id)

        # kafka 호출
        producer = MessageProducer()
        producer.send(topic='post', message=str(user.id))
        producer.send(topic='es', message={
            "user": post.user.username,
            "text": post.text,
        })

        urls = []
        for image in images:
            url = create_presigned_url(user_id=user.pk, post_id=post.id, file_name=image)
            urls.append(url)

        validated_data['urls'] = urls
        validated_data['id'] = post.id
        return validated_data


class PostReadSerializer(PostSerializer):
    username = serializers.ReadOnlyField(source='user.username')
    comments = SimpleCommentSerializer(many=True)
    images = ImageSerializer(many=True)
    likes = LikeReadSerializer(many=True)
    likes_count = serializers.SerializerMethodField()

    class Meta:
        model = Post
        fields = ['id', 'text', 'user', 'username', 'images', 'comments', 'likes', 'likes_count', 'created_at']

    def get_likes_count(self, obj):
        return obj.likes.count()


class PostImageUpdateSerializer(serializers.ModelSerializer):
    urls = serializers.ListField(child=serializers.CharField(), write_only=True)

    class Meta:
        model = Post
        fields = ['urls']

    def update(self, instance, validated_data):
        urls = validated_data.get('urls', [])

        for url in urls:
            Image.objects.create(post=instance, url=url)

        return instance


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
