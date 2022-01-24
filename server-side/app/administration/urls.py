from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from administration import views

router = DefaultRouter()
router.register('progress', views.ProgressViewSet)

app_name = 'administration'

urlpatterns = [
    path('', include(router.urls)),
    path('grade/<int:pk>/', views.GradeApiView().as_view(), name='grade'),
    path('course/', views.CourseApiView().as_view(), name='course'),
    path('course/<int:pk>/', views.CourseDetailApiView().as_view(), name='course-detail'),
]