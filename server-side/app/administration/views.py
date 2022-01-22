from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Progress
from administration import serializers
from administration.permissions import AdministratorOrReadOnly

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
        elif self.request.user.role == 1:
            return self.queryset.all()


