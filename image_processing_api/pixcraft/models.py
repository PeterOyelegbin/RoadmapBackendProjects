from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


# Create your models here.
class Picture(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    image = models.ImageField()
    uploaded_at = models.DateTimeField(auto_now_add=True)
    edited_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name
    