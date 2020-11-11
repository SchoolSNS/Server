from django.db import models
from django.conf import settings
from feedAPI.models import Post

class DeviceToken (models.Model) :
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    device_token = models.CharField(max_length=255)

    def __str__ (self) :
        return self.user.username

class Description (models.Model) :
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='description')
    notification_title = models.CharField(max_length=255)

    def __str__ (self) :
        return self.post.title