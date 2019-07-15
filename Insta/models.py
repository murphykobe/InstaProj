from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser
# Create your models here.

class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True,
    )

    def get_followings(self):
        following = UserConnection.objects.filter(creator=self)
        return following

    def get_followers(self):
        followers = UserConnection.objects.filter(following=self)
        return followers

    def is_followed_by(self, user):
        return UserConnection.objects.filter(following=self).filter(creator=user).exists()

    def get_absolute_url(self):
        return reverse("user_profile", args=[str(self.id)])

    def __str__ (self):
        return self.username

class UserConnection(models.Model):
    creator = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="creators"
    )
    following = models.ForeignKey(
        InstaUser,
        on_delete=models.CASCADE,
        related_name="followers"
    )
    def __str__(self):
        return self.creator.username + 'follows' +self.followers.username


class Post(models.Model):
    author= models.ForeignKey(
        InstaUser, 
        on_delete=models.CASCADE,
        related_name='posts',
        blank = True,
        null = True)
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True,
    )
    def get_absolute_url(self):
        return reverse("post_details", args=[str(self.id)])
    
    def __str__(self):
        return self.title
    
    def get_like_count(self):
        return self.likes.count()
        
    def get_comment_count(self):
        return self.comments.count()

class Comment(models.Model):
    post = models.ForeignKey(Post,
            on_delete=models.CASCADE,
            related_name='comments')
    user = models.ForeignKey(InstaUser,
            on_delete=models.CASCADE,
            related_name='comments')
    comment = models.CharField(max_length=100)
    posted_on = models.DateTimeField(
            auto_now_add=True,
            editable=False
    )
    def __str__(self):
        return self.comment


class Like(models.Model):
    post = models.ForeignKey(Post,
            on_delete=models.CASCADE,
            related_name='likes')
    user = models.ForeignKey(InstaUser,
            on_delete=models.CASCADE,
            related_name='likes')
    def __str__(self):
        return 'Like: '+ self.user.username + ' Likes ' + self.post.title
    