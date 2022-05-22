from django.contrib import admin
from .models import (Student, StudentGroup, Stage, Specialization, Discipline,
                     FormOfControl, AcademicWork, Approach, Teacher, MyUser, TemplateStage, NameTemplate)


# Register your models here.
@admin.register(MyUser)
class MyUserAdmin(admin.ModelAdmin):
    list_display = ['id', 'first_name', 'last_name', 'surname', 'user_type',
                    'username', 'email']


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ['user', 'num_z']


@admin.register(StudentGroup)
class StudentGroupAdmin(admin.ModelAdmin):
    list_display = ['group_id', 'name', 'specialization_id']


@admin.register(Stage)
class StageAdmin(admin.ModelAdmin):
    list_display = ['name', 'academic_work_id', 'parent_stage_id']


@admin.register(Specialization)
class SpecializationAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(Teacher)
class TeacherAdmin(admin.ModelAdmin):
    list_display = ['pk', 'user']


@admin.register(Discipline)
class DisciplineAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(FormOfControl)
class FormOfControlAdmin(admin.ModelAdmin):
    list_display = ['name']


@admin.register(AcademicWork)
class AcademicWorkAdmin(admin.ModelAdmin):
    list_display = ['academic_work_id', 'name', 'student_id', 'discipline_id', 'form_of_control_id']


@admin.register(Approach)
class ApproachAdmin(admin.ModelAdmin):
    list_display = ['stage_id', 'name', 'comment', 'date']


@admin.register(TemplateStage)
class TemplateStageAdmin(admin.ModelAdmin):
    list_display = ['stage_id', 'name', 'parent_id', 'duration', 'template_id']


@admin.register(NameTemplate)
class NameTemplateAdmin(admin.ModelAdmin):
    list_display = ['template_id', 'name', 'teacher_id']
