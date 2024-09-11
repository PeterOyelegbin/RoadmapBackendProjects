from django.db import models
from uuid import uuid4

# Create your models here.
class MarkDown(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    filename = models.CharField(max_length=255)
    file = models.FileField(upload_to='./mkd_note_taking_app/static/md_files/')

    def __str__(self):
        return self.filename
