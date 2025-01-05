from rest_framework import viewsets, status
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework.permissions import IsAuthenticated
from drf_yasg.utils import swagger_auto_schema
from PIL import Image, ImageOps, ImageEnhance, UnidentifiedImageError
from io import BytesIO
from django.core.files.base import ContentFile
from utils import general_logger
from .serializers import Picture, PictureSerializer, TransformSerializer, ResizeSerializer, CropSerializer, FilterSerializer
import os


# Create your views here.
class ImageViewSet(viewsets.ModelViewSet):
    """Manage images in the database"""
    queryset = Picture.objects.all()
    serializer_class = PictureSerializer
    parser_classes = [MultiPartParser, FormParser]
    permission_classes = [IsAuthenticated]
    http_method_names = ['get', 'post', 'put', 'delete']

    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT_FOUND', 500: 'SERVER ERROR'})
    def list(self, request, *args, **kwargs):
        try:
            instance = self.queryset.all()
            if not instance:
                raise Picture.DoesNotExist
            serializer = self.serializer_class(instance, many=True)
            response_data = {
                'status': 200,
                'success': True,
                'message': 'Images retrieved successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Picture.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'No images found!',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error(f"Error retrieving images: {e}")
            response_data = {
                'status': 500,
                'success': False,
                'message': 'An error during image retrieval! Please try again',
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(request_body=PictureSerializer, responses={201: 'CREATED', 400: 'BAD REQUEST'})
    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        try:
            serializer.is_valid(raise_exception=True)
            user = request.user
            image_file = serializer.validated_data['image']
            # Remove the file extension from the image name
            name, _ = os.path.splitext(image_file.name)
            serializer.save(user=user, name=name)
            response_data = {
                'status': 201,
                'success': True,
                'message': 'Image uploaded successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_201_CREATED)
        except Exception as e:
            general_logger.error(f"Error uploading image: {e}")
            response_data = {
                'status': 400,
                'success': False,
                'message': 'An error during image upload!',
            }
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    @swagger_auto_schema(responses={200: 'OK', 404: 'NOT_FOUND', 500: 'SERVER ERROR'})
    def retrieve(self, request, pk=None):
        try:
            instance = self.queryset.get(id=pk)
            if not instance:
                raise Picture.DoesNotExist
            serializer = self.get_serializer(instance)
            response_data = {
                'status': 200,
                'success': True,
                'message': 'Image details retrieved successfully',
                'data': serializer.data
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Picture.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Image not found!',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error(f"Error retrieving image: {e}")
            response_data = {
                'status': 500,
                'success': False,
                'message': 'An error during image retrieval! Please try again',
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(request_body=TransformSerializer, responses={200: 'OK', 404: 'NOT_FOUND', 500: 'SERVER ERROR'})
    @action(detail=True, methods=['put'], url_path='transform')
    def transform(self, request, pk=None):
        try:
            serializer = TransformSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            rotate = serializer.validated_data.get('rotate')
            format = serializer.validated_data.get('format')
            # Retrieve the image file from the database
            instance = self.queryset.get(id=pk)
            image_file = instance.image
            img = Image.open(image_file)
            # Apply transformations
            if rotate != 0:
                angle = rotate
                img = img.rotate(angle)
                # Save the transformed image to a BytesIO object
                img_io = BytesIO()
            if format in ['jpeg', 'jpg', 'png']:
                img_format = format
                # Save the transformed image to a BytesIO object
                img_io = BytesIO()
            img_format = img.format or "JPEG"  # Default to JPEG if format is missing
            img.save(img_io, format=img_format)
            file_name = image_file.name
            img_content = ContentFile(img_io.getvalue(), name=file_name)
            # Delete existing image file from the database
            image_file.delete(save=False)
            # Update the image object with the transformed image
            instance.image.save(file_name, img_content)
            instance.save()
            response_data = {
                'status': 200,
                'success': True,
                'message': 'Image transformed successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Picture.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Image not found!',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error(f"Error transforming image: {e}")
            response_data = {
                'status': 500,
                'success': False,
                'message': 'An error occurred during image transformation!',
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
    @swagger_auto_schema(responses={204: 'NO_CONTENT', 404: 'NOT_FOUND', 500: 'SERVER ERROR'})
    def destroy(self, request, pk=None):
        try:
            instance = self.queryset.get(id=pk)
            if not instance:
                raise Picture.DoesNotExist
            instance.image.delete()
            instance.delete()
            response_data = {
                'status': 204,
                'success': True,
                'message': 'Image deleted successfully',
            }
            return Response(response_data, status=status.HTTP_204_NO_CONTENT)
        except Picture.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Image not found!',
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error(f"Error deleting image: {e}")
            response_data = {
                'status': 500,
                'success': False,
                'message': 'An error occured during image deletion!',
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class ResizeImageView(viewsets.ViewSet):
    """Resize image in the database"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=ResizeSerializer, responses={200: 'OK', 404: 'NOT_FOUND', 500: 'SERVER ERROR'})
    @action(detail=True, methods=['put'], url_path='resize')
    def resize(self, request, pk=None):
        try:
            serializer = ResizeSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            width = serializer.validated_data['width']
            height = serializer.validated_data['height']
            # Retrieve the image file from the database
            instance = Picture.objects.get(id=pk)
            image_file = instance.image
            # Open the image using Pillow
            try:
                img = Image.open(image_file)
            except UnidentifiedImageError:
                raise ValueError("The image format is unsupported or the file is corrupted.")
            img = img.resize((width, height))
            # Save the resized image to a BytesIO object
            img_io = BytesIO()
            img_format = img.format or "JPEG"  # Default to JPEG if format is missing
            img.save(img_io, format=img_format)
            file_name = image_file.name
            img_content = ContentFile(img_io.getvalue(), name=file_name)
            # Delete existing image file from the database
            image_file.delete(save=False)
            # Update the image object with the resized image
            instance.image.save(file_name, img_content)
            instance.save()
            response_data = {
                'status': 200,
                'success': True,
                'message': 'Image resized successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Picture.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Image not found!'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error(f"Error transforming image: {e}")
            response_data = {
                'status': 500,
                'success': False,
                'message': 'An error occurred during image transformation!'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class CropImageView(viewsets.ViewSet):
    """Crop image in the database"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=CropSerializer, responses={200: 'OK', 404: 'NOT_FOUND', 500: 'SERVER ERROR'})
    @action(detail=True, methods=['put'], url_path='crop')
    def crop(self, request, pk=None):
        try:
            serializer = CropSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            width = serializer.validated_data['width']
            height = serializer.validated_data['height']
            x = serializer.validated_data['x']
            y = serializer.validated_data['y']
            # Retrieve the image file from the database
            instance = Picture.objects.get(id=pk)
            image_file = instance.image
            # Open the image using Pillow
            try:
                img = Image.open(image_file)
            except UnidentifiedImageError:
                raise ValueError("The image format is unsupported or the file is corrupted.")
            img = img.crop((x, y, x + width, y + height))
            # Save the croped image to a BytesIO object
            img_io = BytesIO()
            img_format = img.format or "JPEG"  # Default to JPEG if format is missing
            img.save(img_io, format=img_format)
            file_name = image_file.name
            img_content = ContentFile(img_io.getvalue(), name=file_name)
            # Delete existing image file from the database
            image_file.delete(save=False)
            # Update the image object with the croped image
            instance.image.save(file_name, img_content)
            instance.save()
            response_data = {
                'status': 200,
                'success': True,
                'message': 'Image cropped successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Picture.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Image not found!'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error(f"Error cropping image: {e}")
            response_data = {
                'status': 500,
                'success': False,
                'message': 'An error occurred during image cropping! Please try again'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        

class FilterImageView(viewsets.ViewSet):
    """Apply filters to image in the database"""
    permission_classes = [IsAuthenticated]

    @swagger_auto_schema(request_body=FilterSerializer, responses={200: 'OK', 404: 'NOT_FOUND', 500: 'SERVER ERROR'})
    @action(detail=True, methods=['put'], url_path='filter')
    def filter(self, request, pk=None):
        try:
            serializer = FilterSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            grayscale = serializer.validated_data.get('grayscale', False)
            sepia = serializer.validated_data.get('sepia', False)
            # Retrieve the image file from the database
            instance = Picture.objects.get(pk=pk)
            image_file = instance.image
            # Open the image using Pillow
            try:
                img = Image.open(image_file)
            except UnidentifiedImageError:
                raise ValueError("The image format is unsupported or the file is corrupted.")
            if grayscale:
                img = ImageOps.grayscale(img)
            if sepia:
                sepia = ImageEnhance.Color(img).enhance(0.3)
                img = ImageOps.colorize(sepia, '#704214', '#C0C0C0')
            # Save the filtered image to a BytesIO object
            img_io = BytesIO()
            img_format = img.format or "JPEG"  # Default to JPEG if format is missing
            img.save(img_io, format=img_format)
            file_name = image_file.name
            img_content = ContentFile(img_io.getvalue(), name=file_name)
            # Delete existing image file from the database
            image_file.delete(save=False)
            # Update the image object with the filtered image
            instance.image.save(file_name, img_content)
            instance.save()
            response_data = {
                'status': 200,
                'success': True,
                'message': 'Image filters applied successfully'
            }
            return Response(response_data, status=status.HTTP_200_OK)
        except Picture.DoesNotExist:
            response_data = {
                'status': 404,
                'success': False,
                'message': 'Image not found!'
            }
            return Response(response_data, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            general_logger.error(f"Error applying image filters: {e}")
            response_data = {
                'status': 500,
                'success': False,
                'message': 'An error occurred during image filtering!'
            }
            return Response(response_data, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        