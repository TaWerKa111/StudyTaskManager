from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist


# Create your models here.
class Specialization(models.Model):
    """ Специальность """
    specialization_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name


class StudentGroup(models.Model):
    """ Группа """
    student_group_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=50)
    specialization_id = models.ForeignKey(Specialization, on_delete=models.CASCADE)

    def __str__(self):
        return self.name


class Student(models.Model):
    """ Студент """
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    patronymic = models.CharField(max_length=50, null=True)
    number_record_book = models.CharField(max_length=10, null=True)
    student_group_id = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, null=True)

    def __str__(self):
        return self.user.get_full_name()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    try:
        instance.student.save()
    except ObjectDoesNotExist:
        Student.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    instance.student.save()


# class Teacher():
#     """ Преподаватель """
#     pass


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
