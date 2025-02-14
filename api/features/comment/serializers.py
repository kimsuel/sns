from rest_framework import serializers

from api.features.comment.models import Comment


class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = '__all__'

    def validate(self, data):
        user = self.context['request'].user
        if user != self.instance.user or user != self.instance.post.user:
            raise serializers.ValidationError('Only the author can edit and delete.')
        return data


class SimpleCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ['id', 'text', 'created_at']
