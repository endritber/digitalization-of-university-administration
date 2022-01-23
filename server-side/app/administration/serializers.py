from user.serializers import UserSerializer
from core.models import Progress
from rest_framework import serializers

 
class ProgressSerializer(serializers.ModelSerializer):
    """Serializer for Progress objects"""
    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ('id',)
        