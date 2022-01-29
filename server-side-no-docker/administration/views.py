from rest_framework.response import Response
from rest_framework import status
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import get_user_model
from core.models import Progress, CourseGrade, Course, Transcript, Examination
from administration import serializers
from administration.permissions import AdministratorOrReadOnly, AdministratorOrProfessorStudentReadOnly, ProfessorOnly, StudentOnly
from rest_framework import generics


class ExaminationViewSet(viewsets.ModelViewSet):
    """Examination for administrator to add to the system"""    
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, AdministratorOrProfessorStudentReadOnly)
    serializer_class = serializers.ExaminationSerializer
    queryset = Examination.objects.all()

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.DetailedExaminationSerializer
        elif self.action == 'list' and self.request.user.role == 2 or self.request.user.role == 3:
            return serializers.DetailedExaminationSerializer
        return self.serializer_class

    def create(self, request, *args, **kwargs):
        id = self.request.data['user']
        user = get_user_model().objects.get(id=id)
        if user.role == 3 or user.role == 1 or user.role == None:
            return Response({'detail':'You cannot add an examination other than a professor.'}, status=status.HTTP_403_FORBIDDEN)
        if Examination.objects.filter(user=user, course=self.request.data['course']).exists():
            return Response({'detail':'This professor already has an examination with this course.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().create(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        id = self.request.data['user']
        user = get_user_model().objects.get(id=id)
        if Examination.objects.filter(user=user, course=self.request.data['course']).exists():
            return Response({'detail':'This professor already has an examination with this course.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class StudentExaminationViewSet(viewsets.GenericViewSet, mixins.RetrieveModelMixin, mixins.UpdateModelMixin):
    """Examination for student"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, StudentOnly)
    serializer_class = serializers.ProgressSerializerStudent
    queryset = Progress.objects.all()

class ProgressViewSet(viewsets.GenericViewSet,
                     mixins.ListModelMixin,
                     mixins.RetrieveModelMixin,
                     mixins.CreateModelMixin,
                     mixins.UpdateModelMixin,
                     mixins.DestroyModelMixin):
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
            return Response({'detail':'You cannot add a progress other than a student.'}, status=status.HTTP_403_FORBIDDEN)
        return super().create(request, *args, **kwargs)


    def update(self, request, *args, **kwargs):
        id = self.request.data['user']
        user = get_user_model().objects.get(id=id)
        if user.role == 2 or user.role == 1 or user.role == None:
            return Response({'detail':'You cannot add a progress other than a student.'}, status=status.HTTP_400_BAD_REQUEST)
        return super().update(request, *args, **kwargs)


class GradeApiView(generics.CreateAPIView):
    """Manage Grade for student"""
    serializer_class = serializers.CourseGradeSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, ProfessorOnly)
    queryset = CourseGrade.objects.all()

    def create(self, request, *args, **kwargs):
        pk = self.kwargs.get('pk')
        try:
            user = get_user_model().objects.get(pk=pk)
        except:
            return Response({'detail':'This student id doesn\'t exits.'}, status=status.HTTP_400_BAD_REQUEST)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if CourseGrade.objects.filter(user=user, course=self.request.data['course']).exists():
            return Response({'detail':'This student already has a grade to this course.'}, status=status.HTTP_400_BAD_REQUEST)
        else:
            self.perform_create(serializer)
            data = {}
            transcript = Transcript.objects.get(user=user.id)
            ser = serializers.TranscriptSerializer(transcript)
            return Response(ser.data, status=status.HTTP_201_CREATED)

    def perform_create(self, serializer):
        pk = self.kwargs.get('pk')
        user = get_user_model().objects.get(pk=pk)
        serializer.save(user=user)


class CourseViewSet(viewsets.ModelViewSet):
    """Courses for student"""
    serializer_class = serializers.CourseSerializer
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated, AdministratorOrProfessorStudentReadOnly)
    queryset = Course.objects.all()