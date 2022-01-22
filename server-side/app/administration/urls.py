from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from administration import views

router = DefaultRouter()
router.register('progress', views.ProgressViewSet)

app_name = 'administration'

urlpatterns = [
    path('', include(router.urls))
]