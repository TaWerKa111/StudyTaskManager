from rest_framework import serializers
from .models import AcademicWork, FormOfControl


class AcademicWorkSerializer(serializers.ModelSerializer):
    class Meta:
        model = AcademicWork
        fields = '__all__'


class FormOfControlSerializer(serializers.ModelSerializer):
    class Meta:
        model = FormOfControl
        fields = '__all__'
