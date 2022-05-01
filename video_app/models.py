from django.db import models
from django.contrib.auth.models import User
import os

def user_directory_path(instance, filename):
    return 'user_{0}/{1}'.format(instance.user.username, filename)

class Media(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=200, null=True, blank=True)
    description = models.TextField()
    media = models.FileField(upload_to=user_directory_path)
    thumbnail = models.ImageField(upload_to=user_directory_path)
    views = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True, auto_now=False)
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)

    def __str__(self):
        return f'{self.user.username} -> {self.title}'
    
    def filename(self):
        return os.path.basename(self.media.name)
    

