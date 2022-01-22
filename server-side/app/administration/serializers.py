from core.models import Progress
from rest_framework import serializers
from user.serializers import UserSerializer

class ProgressSerializer(serializers.ModelSerializer):
    """Serializer for Progress objects"""
    user = UserSerializer()
    class Meta:
        model = Progress
        fields = ('id', 'degree', 'user')
        read_only_fields = ('id','user')
        