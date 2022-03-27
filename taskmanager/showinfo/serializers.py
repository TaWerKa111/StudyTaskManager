from rest_framework import serializers
from auth_user.models import Stage, Teacher, \
    Discipline, FormOfControl, \
    AcademicWork, Approach, \
    Student, Specialization, StudentGroup

from .models import TemplateStage, NameTemplate


class StageSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Этап """
    class Meta:
        model = Stage
        fields = '__all__'


class StudentGroupSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Группа студентов """
    class Meta:
        model = StudentGroup
        fields = '__all__'


class StudentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Student
        fields = '__all__'


class DisciplineSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Дисциплина """
    class Meta:
        model = Discipline
        fields = '__all__'


class FormOfControlSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Форма контроля """
    class Meta:
        model = FormOfControl
        fields = '__all__'


class AcademicWorkSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Учебная работа """
    class Meta:
        model = AcademicWork
        fields = '__all__'


class AcademicWorkWithStudentSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Учебная работа  и студент"""
    student_id = StudentSerializer(read_only=True)

    class Meta:
        model = AcademicWork
        fields = '__all__'


class ApproachSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Поход """
    model1 = StageSerializer(read_only=True)

    class Meta:
        model = Approach
        fields = "__all__"


class TeacherSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Преподаватель """
    class Meta:
        model = Teacher
        fields = '__all__'


class SpecializationSerializer(serializers.ModelSerializer):
    """ Сериализатор для модели Специальность """

    class Meta:
        model = Specialization
        fields = '__all__'


class TemplateStageSerializer(serializers.ModelSerializer):

    class Meta:
        model = TemplateStage
        fields = '__all__'

    # def create(self, validated_data):
    #     return NameTemplate.objects.create(**validated_data)


class NameTemplateStageSerializer(serializers.ModelSerializer):
    # template_stage = TemplateStageSerializer(read_only=True)

    class Meta:
        model = NameTemplate
        fields = '__all__'