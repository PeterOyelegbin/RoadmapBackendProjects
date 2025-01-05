from rest_framework import serializers
from .models import Picture


class PictureSerializer(serializers.ModelSerializer):
    class Meta:
        model = Picture
        fields = '__all__'
        read_only_fields = ('id', 'user', 'name', 'uploaded_at', 'edited_at')


class TransformSerializer(serializers.Serializer):
    rotate = serializers.IntegerField()
    format = serializers.ChoiceField(choices=['-','jpeg', 'jpg', 'png'])
    

class ResizeSerializer(serializers.Serializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField()


class CropSerializer(serializers.Serializer):
    width = serializers.IntegerField()
    height = serializers.IntegerField()
    x = serializers.IntegerField()
    y = serializers.IntegerField()


class FilterSerializer(serializers.Serializer):
    grayscale = serializers.BooleanField()
    sepia = serializers.BooleanField()
