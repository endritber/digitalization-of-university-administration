from core.models import Progress
from rest_framework import serializers
from user.serializers import UserSerializer

class ProgressSerializer(serializers.ModelSerializer):
    """Serializer for Progress objects"""
    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ('id',)
        