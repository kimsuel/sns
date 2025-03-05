from rest_framework import serializers

from api.features.follow.models import Follow
from api.user.models import User


class FollowSerializer(serializers.ModelSerializer):
    follower_name = serializers.CharField(write_only=True)
    followee_name = serializers.CharField(write_only=True)

    def create(self, validated_data):
        follower_name = validated_data.pop('follower_name')
        follower = User.objects.get(username=follower_name)
        followee_name = validated_data.pop('followee_name')
        followee = User.objects.get(username=followee_name)

        kwargs = {
            'follower': follower,
            'followee': followee
        }
        instance = super(FollowSerializer, self).create(kwargs)
        return instance

    class Meta:
        model = Follow
        fields = '__all__'
        read_only_fields = ('follower', 'followee')


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
