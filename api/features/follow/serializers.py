from rest_framework import serializers

from api.features.follow.models import Follow


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
