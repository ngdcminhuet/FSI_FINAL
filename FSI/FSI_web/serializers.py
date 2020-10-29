from rest_framework import serializers
from .models import Post, Comments,Project, FSI_user
from rest_framework_jwt.settings import api_settings

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


class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = FSI_user
        fields = ('username',)


class UserSerializerWithToken(serializers.ModelSerializer):

    token = serializers.SerializerMethodField()
    password = serializers.CharField(write_only=True)

    def get_token(self, obj):
        jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
        jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER

        payload = jwt_payload_handler(obj)
        token = jwt_encode_handler(payload)
        return token

    def create(self, validated_data):
        password = validated_data.pop('password', None)
        instance = self.Meta.model(**validated_data)
        if password is not None:
            instance.set_password(password)
        instance.save()
        return instance

    class Meta:
        model = FSI_user
        fields = ('token', 'username', 'password')




class SocialSerializer(serializers.Serializer):

    provider = serializers.CharField(max_length=255, required=True)
    access_token = serializers.CharField(max_length=4096, required=True, trim_whitespace=True)