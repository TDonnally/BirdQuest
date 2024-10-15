from django.db import models

from django.db import models
from django.contrib.auth.models import User

class BirdsFound(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    bird_name = models.CharField(max_length=255)
    uploaded_image = models.CharField(max_length=255) 
    found_count = models.IntegerField(default=1)
    created_at = models.DateTimeField(auto_now_add=True)

class UsersBirdCollection(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    total_birds_found = models.IntegerField(default=0)