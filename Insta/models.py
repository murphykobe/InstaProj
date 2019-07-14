from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
from django.contrib.auth.models import AbstractUser
# Create your models here.

class Post(models.Model):
    title = models.TextField(blank=True, null=True)
    image = ProcessedImageField(
        upload_to = 'static/images/posts',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True,
    )
    def get_absolute_url(self):
        ##return reverse("post_details", kwargs={"pk": self.pk})
        return reverse("post_details", args=[str(self.id)])
    
    def __str__(self):
        return self.title

class InstaUser(AbstractUser):
    profile_pic = ProcessedImageField(
        upload_to = 'static/images/profiles',
        format = 'JPEG',
        options = {'quality': 100},
        blank = True,
        null = True,
    )