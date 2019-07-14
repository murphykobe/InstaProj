from django.db import models
from django.urls import reverse
from imagekit.models import ProcessedImageField
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
