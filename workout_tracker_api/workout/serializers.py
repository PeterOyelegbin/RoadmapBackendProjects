from rest_framework import serializers
from .models import Exercise, Plan, Session


class ExerciseSerializer(serializers.ModelSerializer):
    class Meta:
        model = Exercise
        fields = "__all__"


class PlanSerializer(serializers.ModelSerializer):
    exercise_id = serializers.CharField(write_only=True)
    exercise = ExerciseSerializer(read_only=True)
    
    class Meta:
        model = Plan
        fields = ("id", "user", "name", "exercise_id", "exercise", "repetitions", "sets", "weight", "comment", "created_at")
        read_only_fields = ["user"]


class SessionSerializer(serializers.ModelSerializer):
    plan_id = serializers.CharField(write_only=True)
    plan = PlanSerializer(read_only=True)
    
    class Meta:
        model = Session
        fields = ("id", "user", "plan_id", "plan", "scheduled_at", "completed_at", "status")
        read_only_fields = ["user"]
