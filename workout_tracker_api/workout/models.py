from django.db import models
from django.contrib.auth.models import User
from uuid import uuid4


# Create your models here.
class Exercise(models.Model):
    CATEGORY_CHOICE = [("cardio", "Cardio"), ("strength", "Strength"), ("flexibility", "Flexibility")]
    
    MUSCLE_CHOICE = [("chest", "chest"), ("back", "back"), ("legs", "legs")]

    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    description = models.TextField()
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICE)
    muscle_group = models.CharField(max_length=50, choices=MUSCLE_CHOICE)

    def __str__(self):
        return self.name
    

class Plan(models.Model):
    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, unique=True, db_index=True)
    exercise = models.ForeignKey(Exercise, on_delete=models.CASCADE)
    repetitions = models.IntegerField()
    sets = models.IntegerField()
    weight = models.FloatField()
    comment = models.TextField()
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return f"{self.user} - {self.name} - {self.created_at}"
    

class Session(models.Model):
    STATUS_CHOICE = [("scheduled", "Scheduled"), ("completed", "Completed"), ("missed", "Missed")]

    id = models.UUIDField(default=uuid4, unique=True, primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    plan = models.ForeignKey(Plan, on_delete=models.CASCADE)
    scheduled_at = models.DateField()
    completed_at = models.DateField()
    status = models.CharField(max_length=50, choices=STATUS_CHOICE)

    def __str__(self):
        return f"{self.user} - {self.plan} - {self.status}"
    