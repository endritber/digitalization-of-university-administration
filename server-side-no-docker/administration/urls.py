from unicodedata import name
from django.urls import path, include
from rest_framework.routers import DefaultRouter
from administration import views

router = DefaultRouter()
router.register('progress', views.ProgressViewSet)
router.register('course', views.CourseViewSet)
router.register('examination', views.ExaminationViewSet)
router.register('submitexam', views.StudentExaminationViewSet)

app_name = 'administration'

urlpatterns = [
    path('', include(router.urls)),
    path('grade/<int:pk>/', views.GradeApiView().as_view(), name='grade'),
]