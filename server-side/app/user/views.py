from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics, authentication, permissions, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.permissions import AdministratorOrProfessorReadOnly, AdministratorOrReadOnly
from django.contrib.auth import get_user_model
from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import viewsets
from user import serializers


class UserViewSet(viewsets.ModelViewSet):
    serializer_class = serializers.UserSerializer
    queryset = get_user_model().objects.all().exclude(role=1).exclude(role=None)
    authentication_classes = (authentication.TokenAuthentication, )
    permission_classes = (permissions.IsAuthenticated, AdministratorOrProfessorReadOnly)

    def get_serializer_class(self):
        if self.action == 'retrieve':
            return serializers.UserDetailSerializer
        elif self.action == 'upload_image':
            return serializers.UserImageSerializer
            
        return self.serializer_class

    @action(methods=['POST'], detail=True, url_path='upload-image')
    def upload_image(self, request, pk=None):
        """Upload an image to a user"""
        user = self.get_object()
        serializer = self.get_serializer(
            user,
            data=request.data
        )
        if serializer.is_valid():
            serializer.save()
            return Response(
                serializer.data,
                status=status.HTTP_200_OK
            )
        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST
        )
    
    def get_queryset(self):
        if self.request.user.role == 1:
            return super().get_queryset()
        elif self.request.user.role == 2:
            return super().get_queryset().exclude(role=2)

class CreateTokenView(ObtainAuthToken):
    """
    Create a new auth token for the user
    """
    serializer_class = AuthTokenSerializer
    renderer_classes = api_settings.DEFAULT_RENDERER_CLASSES


class ManageUserView(generics.RetrieveUpdateAPIView):
    """
    Manage the authenticated user
    """
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, AdministratorOrReadOnly)

    def get_object(self):
        """
        Retrieve and return authenticated user
        """
        return self.request.user
