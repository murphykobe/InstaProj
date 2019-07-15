
from django.shortcuts import render
from rest_framework import generics
from API.serializers import PostSerializer,CreateSerializer
from Insta.models import Post
# Create your views here.
 

class PostAPIView(generics.ListAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer

class CreateAPIView(generics.CreateAPIView):
   queryset = Post.objects.all()
   serializer_class = CreateSerializer

