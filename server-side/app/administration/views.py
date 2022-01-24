from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from core.models import Progress, CourseGrade, Course
from administration import serializers
from administration.permissions import AdministratorOrReadOnly, ProfessorPermission
from rest_framework import generics

class ProgressViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin):
    """Manage Progress in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, AdministratorOrReadOnly)
    serializer_class = serializers.ProgressSerializer
    queryset = Progress.objects.all()


    def get_queryset(self):
        if self.request.user.role == 3:
            return self.queryset.filter(user=self.request.user)
        else:
            return self.queryset.all()

    def create(self, request, *args, **kwargs):
        id = self.request.data['user']
        user = get_user_model().objects.get(id=id)
        if user.role == 2 or user.role == 1 or user.role == None:
            return Response({'detail':'You cannot add a progress other than a student'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)

class GradeApiView(generics.CreateAPIView):
    """Manage Grade for student"""

    serializer_class = serializers.CourseGradeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, ProfessorPermission)
    queryset = CourseGrade.objects.all()

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        user = get_user_model().objects.get(pk=pk)
        if CourseGrade.objects.filter(user=user, course=self.request.data['course']).exists():
            return Response({'detail':'This student already has a grade to this course.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            serializer.save(user=user)

class CourseApiView(generics.ListAPIView,):
    """Courses for student"""

    serializer_class = serializers.CourseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, ProfessorPermission)
    queryset = Course.objects.all()

class CourseDetailApiView(generics.RetrieveAPIView):
    """Courses for student"""

    serializer_class = serializers.CourseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, ProfessorPermission)
    queryset = Course.objects.all()

