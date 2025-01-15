from rest_framework import serializers

from api.features.models import Post, Image, Comment, Like, Follow, Bookmark


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
    following_name = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ['id', 'follower', 'follower_name', 'following', 'following_name']


class FollowerSerializer(serializers.ModelSerializer):
    user_id = serializers.ReadOnlyField(source='following.id')
    username = serializers.ReadOnlyField(source='following.username')

    class Meta:
        model = Follow
        fields = ['user_id', 'username']


class FollowingSerializer(serializers.ModelSerializer):
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
        fields = ['id', 'image']


class PostSerializer(serializers.ModelSerializer):
    images = serializers.ListField(child=serializers.ImageField(), write_only=True)

    class Meta:
        model = Post
        fields = ['text', 'user', 'images']

    def create(self, validated_data):
        user = validated_data.get('user')
        images = validated_data.pop('images', [])
        post = Post.objects.create(**validated_data)

        for image in images:
            img_instance = Image.objects.create(image=image, user=user)
            post.images.add(img_instance)

        return post


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
