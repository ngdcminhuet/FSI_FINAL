from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from django.http import JsonResponse
from rest_framework.permissions import AllowAny
from .models import Post, Comments,Project
from .serializers import GetPostSerialize, GetCommentsSerialize, PostProjectSerializer, SocialSerializer
from urllib.error import HTTPError
from rest_framework_jwt.settings import api_settings
jwt_payload_handler = api_settings.JWT_PAYLOAD_HANDLER
jwt_encode_handler = api_settings.JWT_ENCODE_HANDLER
from django.contrib.auth import authenticate, login
from rest_framework import generics, permissions, status, views
from rest_framework.response import Response
from requests.exceptions import HTTPError

from social_django.utils import load_strategy, load_backend
from social_core.backends.oauth import BaseOAuth2
from social_core.exceptions import MissingBackend, AuthTokenError, AuthForbidden
# Create your views here.

class GetPostMostLikesView(APIView):

    def get(self,request):
        list_post= Post.objects.order_by('-num_likes')[:1]
        mydata = GetPostSerialize(list_post, many=True)
        return Response(data=mydata.data, status = status.HTTP_200_OK)

class GetPostMostsShareView(APIView):

    def get(self,request):
        list_post= Post.objects.order_by('-num_shares')[:1]
        mydata = GetPostSerialize(list_post, many=True)
        return Response(data=mydata.data, status = status.HTTP_200_OK)

class GetCommentsView(APIView):

    def get(self,request):
        list_comments= Comments.objects.order_by('-num_likes')[:1]
        mydata = GetCommentsSerialize(list_comments, many=True)
        return Response(data=mydata.data, status = status.HTTP_200_OK)

class PostProjectView(APIView):
    def post(self,request):
        mydata = PostProjectSerializer(request.data)
        if not mydata.is_valid:
            return Response('khong hop le', status=status.HTTP_400_BAD_REQUEST)
        project_name= mydata.data['project_name']
        content = mydata.data['content']
        start_time = mydata.data['start_time']
        end_time = mydata.data['end_time']
        company = mydata.data['company']
        new_project = Project.objects.create(id = 1,project_name = project_name, content =content, start_time=start_time, end_time=end_time, company=company)
        return Response('ok', status=status.HTTP_200_OK)


class SocialLoginView(generics.GenericAPIView):
    """Log in using facebook"""
    serializer_class = SocialSerializer
    permission_classes = [AllowAny]

    def post(self, request):
        """Authenticate user through the provider and access_token"""
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        provider = serializer.data.get('provider', None)
        strategy = load_strategy(request)

        try:
            backend = load_backend(strategy=strategy, name=provider,
                                   redirect_uri=None)

        except MissingBackend:
            return Response({'error': 'Please provide a valid provider'},
                            status=status.HTTP_400_BAD_REQUEST)
        try:
            if isinstance(backend, BaseOAuth2):
                access_token = serializer.data.get('access_token')
            user = backend.do_auth(access_token)
        except HTTPError as error:
            return Response({
                "error": {
                    "access_token": "Invalid token",
                    "details": str(error)
                }
            }, status=status.HTTP_400_BAD_REQUEST)
        except AuthTokenError as error:
            return Response({
                "error": "Invalid credentials",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        try:
            authenticated_user = backend.do_auth(access_token, user=user)

        except HTTPError as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        except AuthForbidden as error:
            return Response({
                "error": "invalid token",
                "details": str(error)
            }, status=status.HTTP_400_BAD_REQUEST)

        if authenticated_user and authenticated_user.is_active:
            # generate JWT token
            login(request, authenticated_user)
            data = {
                "token": jwt_encode_handler(
                    jwt_payload_handler(user)
                )}
            # customize the response to your needs
            response = {
                "email": authenticated_user.email,
                "username": authenticated_user.username,
                "token": data.get('token')
            }
            return Response(status=status.HTTP_200_OK, data=response)


social_auth = SocialLoginView.as_view()