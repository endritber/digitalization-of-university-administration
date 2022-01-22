from rest_framework import viewsets, mixins
from rest_framework.authentication import TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from core.models import Progress
from administration import serializers

class ProgressViewSet(viewsets.GenericViewSet, mixins.ListModelMixin):
    """Manage Progress in the database"""
    authentication_classes = (TokenAuthentication,)
    permission_classes = (IsAuthenticated,)
    serializer_class = serializers.ProgressSerializer
    queryset = Progress.objects.all()


    def get_queryset(self):
        return self.queryset.filter(user=self.request.user)