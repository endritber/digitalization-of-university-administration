from django.shortcuts import get_object_or_404
from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Progress
from administration import serializers
from administration.permissions import AdministratorOrReadOnly
from rest_framework.response import Response

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
    # def retrieve(self, request, *args, **kwargs):
    #     queryset = Progress.objects.all()
    #     progress = get_object_or_404(queryset, user=self.kwargs['pk'])
    #     serializer = self.get_serializer(progress)
    #     return Response(serializer.data)

    # def update(self, request, *args, **kwargs):
    #     return super().update(request, *args, **kwargs)
 