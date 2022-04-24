from datetime import datetime, timedelta

import jwt

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators

from .managers import MyUserManager


class MyUser(AbstractBaseUser, PermissionsMixin):
    USER_TYPES = (
        ('Student', 'Student'),
        ('Teacher', 'Teacher')
    )

    first_name = models.CharField(max_length=120)
    last_name = models.CharField(max_length=120)
    surname = models.CharField(max_length=120)

    username = models.CharField(max_length=255)
    email = models.EmailField(validators=[validators.validate_email], unique=True)

    is_staff = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    # is_superuser = models.BooleanField(default=False)

    user_type = models.CharField(max_length=120, choices=USER_TYPES)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    objects = MyUserManager()

    def __str__(self) -> str:
        return str(self.username)

    def get_full_name(self):
        return f'{self.first_name} {self.last_name} {self.surname}'

    @property
    def token(self):
        return self._generate_jwt_token()

    def get_short_name(self):
        return f'{self.last_name} {self.first_name}'

    def _generate_jwt_token(self):
        dt = datetime.now() + timedelta(days=60)

        token = jwt.encode(
            {
                'id': self.pk,
                'type_user': self.user_type,
                'exp': int(dt.strftime('%s')),
            },
            settings.SECRET_KEY, algorithm='HS256'
        )
        return jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])


class Specialization(models.Model):
    """
    Специальность

    Атрибуты:
        - specialization_id: primary key
        - name: название специальности
    """
    specialization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    """
    Группа

    Атрибуты:
        - group_id: primary key
        - name: название группы
        - specialization_id: внешний ключ к таблице Specialization
    """
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    """
    Студент

    Атрибуты:
        - user: внешний ключ с таблицей User
        - num_z: номер зачетной книжки
        - group_id: внешний ключ к таблице StudentGroup
    """
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    num_z = models.CharField(max_length=10)
    group_id = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)

    def __str__(self) -> str:
        return f'{self.user.first_name} {self.user.last_name}'


class Teacher(models.Model):
    """
    Преподаватель

    Атрибуты:
        - user: внешний ключ к таблице User
    """
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Discipline(models.Model):
    """
    Дисциплина

    Атрибуты:
        - discipline_id: primary key
        - name: название дисциплины
    """
    discipline_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FormOfControl(models.Model):
    """
    Тип работы. Форма контроля.

    Атрибуты:
        - form_of_control_id: primary key
        - name: название формы контроля (РГР, Курсовая)
    """
    form_of_control_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AcademicWork(models.Model):
    """
    Учебная работа

    Атрибуты:
        - academic_work_id: primary key
        - name: название учебной работы
        - student_id: внешний ключ к таблице Student
        - discipline_id: внешний ключ к таблице Discipline
        - form_of_control_id: внешний ключ к таблице FromOfControl
        - is_complited: закончена работа или нет.
    """
    academic_work_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    form_of_control_id = models.ForeignKey(FormOfControl, on_delete=models.CASCADE)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE, null=True)
    is_complited = models.BooleanField(default=False)

    def __str__(self):
        return self.name


class Stage(models.Model):
    """
    Этап работы

    Атрибуты:
        - stage_id: primary key
        - name: название этапа работы
        - academic_work_id: внешний ключ к таблице AcademicWork
        - parent_stage_id: Является ли данный этап подэтапом (Если None - то данный этап родитель)
        - is_pass: сдан ли данный этап (True - да, False - нет)
        - planned_data: планируема дата сдачи
        - actually_date: действительная дата сдача (т.е. день в который сдали работу)
    """
    stage_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    academic_work_id = models.ForeignKey(AcademicWork, on_delete=models.CASCADE)
    parent_stage_id = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE)
    is_pass = models.BooleanField(default=False)
    planned_date = models.DateField(default=datetime.today)
    actually_date = models.DateField(null=True, default=datetime.today)

    def __str__(self):
        return self.name


class Approach(models.Model):
    """
    Подходы

    Атрибуты:
        - approach_id: primary key
        - stage_id: внешний ключ к таблице этап
        - name: название подхода
        - comment: комментарий к подходу
        - data: дата сдачи подхода
    """
    approach_id = models.AutoField(primary_key=True)
    stage_id = models.ForeignKey(Stage, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=50)
    date = models.DateField(default=datetime.today)

    def __str__(self):
        return self.name


class NameTemplate(models.Model):
    """
    Название шаблона

    Атрибуты:
        - template_id: primary key
        - name: название шаблона
        - teacher_id: внешний ключ к таблице Teacher
    """
    template_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    teacher_id = models.ForeignKey(Teacher, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def print_name(self):
        print(self.name)


class TemplateStage(models.Model):
    """
    Шаблоны самих этапов

    Атрибуты:
        - stage_id: primary key
        - parent_id: ссылка на stage_id, родителя, если данный этап является дочерним, иначе none
        - name: название этапа
        - duration_id: продолжительность этапа
        - template_id: внешний ключ к таблице NameTemplate
    """
    stage_id = models.AutoField(primary_key=True)
    parent_id = models.ForeignKey('self', null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    duration = models.IntegerField(default=30)

    template_id = models.ForeignKey(NameTemplate, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
