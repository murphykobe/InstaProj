from Insta.models import Post,InstaUser
from rest_framework import serializers




class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author','title','posted_on',)


class CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('author','title','image',)


