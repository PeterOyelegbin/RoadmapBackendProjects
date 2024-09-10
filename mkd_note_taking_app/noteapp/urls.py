"""
URL configuration for noteapp project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
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
from django.urls import path
from notes import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('notes/', views.list_markdown, name='list-markdown'),
    path('notes/upload/', views.upload_markdown, name='upload-markdown'),
    path('notes/check_grammar/<str:file_id>', views.check_grammar, name='check-grammar'),
    path('notes/render_note/<str:file_id>/', views.render_note, name='render-note'),
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
