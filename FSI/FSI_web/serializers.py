from rest_framework import serializers
from .models import Post, Comments,Project

class GetPostSerialize(serializers.ModelSerializer):

    class Meta:
        model = Post
        fields = ('content', 'num_likes', 'num_shares', 'num_comments', 'time_create')

class GetCommentsSerialize(serializers.ModelSerializer):

    class Meta:
        model = Comments
        fields = ('content', 'num_likes', 'time_create', 'author')


class PostProjectSerializer(serializers.Serializer):
    project_name = serializers.CharField(max_length=255)
    content = serializers.CharField(max_length=255)
    start_time = serializers.DateTimeField()
    end_time = serializers.DateTimeField()
    company = serializers.CharField(max_length=200)