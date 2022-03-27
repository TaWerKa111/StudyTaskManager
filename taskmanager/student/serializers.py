from rest_framework import serializers
from .models import AcademicWork


class AcademicWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicWork
        fields = '__all__'

