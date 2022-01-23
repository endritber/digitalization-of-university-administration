from .serializers import UserSerializer, AuthTokenSerializer
from rest_framework import generics, authentication, permissions
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.settings import api_settings
from user.permissions import AdministratorOrReadOnly, AdministratorOrStudentReadOnly
from django.contrib.auth import get_user_model

class CreateUserView(generics.ListCreateAPIView):
    """
    Create a new user in the system
    """
    serializer_class = UserSerializer
    queryset = get_user_model().objects.exclude(role=1).exclude(role=None).order_by('role')
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, AdministratorOrReadOnly)


class RetrieveUserView(generics.RetrieveUpdateAPIView):
    serializer_class = UserSerializer
    authentication_classes = (authentication.TokenAuthentication,)
    permission_classes = (permissions.IsAuthenticated, AdministratorOrReadOnly)
    queryset = get_user_model().objects.exclude(role=1).exclude(role=None).order_by('role')



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
    permission_classes = (permissions.IsAuthenticated, AdministratorOrStudentReadOnly)

    def get_object(self):
        """
        Retrieve and return authenticated user
        """
        return self.request.user
