from django.contrib import admin
from .models import Exercise, Plan, Session

# Register your models here.
@admin.register(Exercise)
class ExerciseAdmin(admin.ModelAdmin):
    list_display = ("id", "name", "description", "category", "muscle_group")
    list_filter = ("category", "muscle_group")
    
@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "name", "exercise", "created_at")
    list_filter = ("user", "created_at")
    
@admin.register(Session)
class SessionAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "plan", "status")
    list_filter = ("user", "status")
    