from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Post, Comments,Project
from .serializers import GetPostSerialize, GetCommentsSerialize, PostProjectSerializer
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