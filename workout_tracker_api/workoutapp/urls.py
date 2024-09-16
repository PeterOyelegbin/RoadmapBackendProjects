"""workoutapp URL Configuration

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
from django.urls import path, re_path
from rest_framework import permissions
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView, TokenVerifyView
from accounts.views import RegisterView, LogoutView
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
   openapi.Info(
      title="Workout Tracker API",
      default_version='v1',
      description="This is a backend system for a workout tracker application where users can sign up, log in, create workout plans, and track their progress with JWT authentication feature.",
      terms_of_service="https://www.google.com/policies/terms/",
      contact=openapi.Contact(email="peteroyelegbin@gmail.com"),
      license=openapi.License(name="BSD License"),
   ),
   public=True,
   permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path('admin/', admin.site.urls),
    path('api/v1/account/register/', RegisterView.as_view(), name='register'),
    path('api/v1/account/login/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/v1/account/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/v1/account/token/verify/', TokenVerifyView.as_view(), name='token_verify'),
    path('api/v1/account/logout/', LogoutView.as_view(), name='logout'),
]
