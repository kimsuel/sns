from rest_framework import serializers

from api.features.comment.serializers import SimpleCommentSerializer
from api.features.like.serializers import LikeReadSerializer
from api.features.post.models import Post, Image
from common.config import create_presigned_url
from common.kafka.producer import MessageProducer


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
        # producer = MessageProducer()
        # producer.send(topic='post', message=str(user.id))
        # producer.send(topic='es', message={
        #     "user": post.user.username,
        #     "post": post.id,
        #     "text": post.text,
        # })

        # kafka connector 이용

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
