from django.conf import settings
from django.urls import path
from . import views
from django.conf.urls.static import static

urlpatterns=[
    path('', views.index, name="index"),
    path('error/', views.incorrect, name="error"),
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)  # to set the media
