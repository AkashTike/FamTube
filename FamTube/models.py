from django.db import models

# Create your models here.
class Video(models.Model):

    published_at = models.DateTimeField()
    title = models.CharField(max_length=100)
    description = models.TextField()
    channel_title = models.CharField(max_length=60)
    thumbnail_url = models.URLField()
    stored_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title