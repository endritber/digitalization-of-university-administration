from core.models import Progress, Transcript, CourseGrade, Course, Examination
from rest_framework import serializers


class CourseSerializer(serializers.ModelSerializer):
    """Serializer for Course"""
    class Meta:
        model= Course
        fields='__all__'

class ExaminationSerializer(serializers.ModelSerializer):
    """Serializer for examination"""
    class Meta:
        model = Examination
        fields = '__all__'

class DetailedExaminationSerializer(serializers.ModelSerializer):
    """Detailed Serializer for examination"""
    course = CourseSerializer()
    user = serializers.StringRelatedField()
    class Meta:
        model = Examination
        fields = '__all__'

class CourseGradeSerializer(serializers.ModelSerializer):
    """Serializer for GradeCourse"""
    class Meta:
        model=CourseGrade
        exclude=('user',)

class TranscriptSerializer(serializers.ModelSerializer):
    """Serializer for Trancsript objects"""
    grade_courses = CourseGradeSerializer(many=True)
    class Meta:
        model = Transcript
        exclude = ('user',)
        read_only_fields = ('id',)

class ProgressSerializer(serializers.ModelSerializer):
    """Serializer for Progress objects"""
    transcript = TranscriptSerializer(read_only=True)
    exams = ExaminationSerializer(read_only=True, many=True)
    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ('id',)
        

class ProgressSerializerStudent(serializers.ModelSerializer):
    """Progress for student to add exam."""
    class Meta:
        model = Progress
        fields = '__all__'
        read_only_fields = ('id','department', 'level', 'user', 'transcript')
        