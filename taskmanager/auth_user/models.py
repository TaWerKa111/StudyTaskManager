from datetime import datetime, timedelta

import jwt

from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.core import validators
from django.utils import timezone

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
        return self.username

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


# Create your models here.
class Specialization(models.Model):
    """ Специальность """
    specialization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    """ Группа """
    group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    """ Студент """
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)
    num_z = models.CharField(max_length=10)
    group_id = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.username


class Teacher(models.Model):
    """ Преподаватель """
    user = models.OneToOneField(MyUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username


class Discipline(models.Model):
    """ Дисциплина """
    discipline_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class FormOfControl(models.Model):
    """ Тип работы. Форма контроля. """
    form_of_control_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class AcademicWork(models.Model):
    """ Учебная работа """
    academic_work_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    student_id = models.ForeignKey(Student, on_delete=models.CASCADE)
    discipline_id = models.ForeignKey(Discipline, on_delete=models.CASCADE)
    form_of_control_id = models.ForeignKey(FormOfControl, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Stage(models.Model):
    """ Этап работы """
    stage_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    academic_work_id = models.ForeignKey(AcademicWork, on_delete=models.CASCADE)
    parent_stage_id = models.ForeignKey('self', on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Approach(models.Model):
    """ Подходы """
    approach_id = models.AutoField(primary_key=True)
    stage_id = models.ForeignKey(Stage, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    comment = models.CharField(max_length=50)
    date = models.DateField()

    def __str__(self):
        return self.name
