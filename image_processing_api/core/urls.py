"""core URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from rest_framework import permissions
from django.conf import settings
from django.conf.urls.static import static
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from accounts.views import SignupView, LoginView, LogoutView
from pixcraft.views import ImageViewSet, ResizeImageView, CropImageView, FilterImageView

# Swagger UI
schema_view = get_schema_view(
   openapi.Info(
      title="Image Processing API",
      default_version='v1',
      description="Image Processing API is a Django-based server-side application that handles user authentication, image management and transformation, and integration with a MySQL database and Amazon S3. It is built using Python, Django Rest Framework, and JWT authentication, providing a robust and scalable image processing service similar to Cloudinary.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(name="Peter Oyelegbin", url="https://peteroyelegbin.com.ng", email="info@peteroyelegbin.com.ng"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

router = DefaultRouter(trailing_slash=False)
router.register(r'accounts/signup', SignupView, basename="auth_signup")
router.register(r'accounts/login', LoginView, basename="auth_login")
router.register(r'accounts/logout', LogoutView, basename="auth_logout")
router.register(r'images/manage', ImageViewSet, basename="manage_images")
router.register(r'images/manage', ResizeImageView, basename="resize_image")
router.register(r'images/manage', CropImageView, basename="crop_image")
router.register(r'images/manage', FilterImageView, basename="filter_image")

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/v1/', include(router.urls)),
    # API DOCS URL
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    