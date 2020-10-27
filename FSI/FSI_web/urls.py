from django.contrib import admin
from django.urls import path,include
from .views import GetPostMostLikesView,GetCommentsView,PostProjectView

urlpatterns = [
    path('get_comments/', GetCommentsView.as_view()),
    path('get_post/', GetPostMostLikesView.as_view()),
    path('post/',PostProjectView.as_view())
]
