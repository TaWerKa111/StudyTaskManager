from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.status import HTTP_200_OK

from .serializers import Stage, StageSerializer
from .serializers import DisciplineSerializer, Discipline
from .serializers import Approach, ApproachSerializer
from .serializers import FormOfControlSerializer, FormOfControl
from .serializers import AcademicWork, AcademicWorkSerializer, AcademicWorkWithStudentSerializer
from .serializers import SpecializationSerializer, Specialization
from .serializers import StudentGroup, StudentGroupSerializer


class StageView(APIView):
    """ Вывод всех этапов по гет запросу """

    def get(self, request):
        stages = Stage.objects.all()
        serializer = StageSerializer(data=stages, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class StudentGroupView(APIView):
    """ Вывод всех студенческих групп """
    def get(self, **kwargs):
        groups = StudentGroup.objects.all()
        serializer = StudentGroupSerializer(data=groups, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SpecializationaView(APIView):

    def get(self, **kwargs):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(data=specializations, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class DisciplineView(APIView):
    """ Вывод всех дисциплин по гет запросу """

    def get(self, request):
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class ApproachView(APIView):
    """ Вывод всех подходов по гет запросу """

    def get(self, request):
        approach = Approach.objects.all()
        serializer = ApproachSerializer(approach, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class FormOfControlView(APIView):
    """ Вывод всех способов проверки знаний по гет запросу """

    def get(self, request):
        form_of_control = FormOfControl.objects.all()
        serializer = FormOfControlSerializer(form_of_control, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class AcademicWorkView(APIView):
    """ Вывод всех академических работ по гет запросу """

    def get(self, request):
        params = request.query_params

        if params:

            group_id = params.get('group_id', None)
            form_of_control_id = params.get('form', None)

            academic_form = AcademicWork.objects.filter(form_of_control_id=form_of_control_id)
            academic_group = AcademicWork.objects.filter(student_id__group_id=group_id)

            academic_ser = AcademicWorkSerializer(academic_form, many=True).data
            academic_ser += AcademicWorkSerializer(academic_group, many=True).data

        else:
            academic_work = AcademicWork.objects.all()
            academic_ser = AcademicWorkSerializer(academic_work, many=True).data

        return Response(academic_ser, status=HTTP_200_OK)


class AcadmicWorkDetailView(APIView):
    """
        Вывод информации по учебной работе вместе с этапами и подходами
        Объединение таблиц Подход и Этап. У каждого этапа может быть несолько под этапов.
        А у каждого подэтапа может быть несколько подходов.

        TODO Вынести логику выполнения запроса к базе данных и форировании ответа в виде JSON
    """

    def get(self, request, pk):
        from copy import deepcopy
        stages = Stage.objects.filter(academic_work_id=pk)
        # stages_id = [stage.stage_id for stage in stages]
        approaches = Approach.objects.filter(stage_id__in=stages)

        stages_ser = StageSerializer(stages, many=True).data
        approaches_ser = ApproachSerializer(approaches, many=True).data

        """ Вынести в отдельную функцию """
        parent_stages = [stage for stage in stages_ser if stage['parent_stage_id'] is None]
        child_stages = [stage for stage in stages_ser if not stage['parent_stage_id'] is None]

        for stage in parent_stages:
            stage['child'] = [child_stage for child_stage in child_stages if
                              stage['stage_id'] == child_stage['parent_stage_id']]

        for parent_stage in parent_stages:
            for child_stage in parent_stage['child']:
                child_stage['apporachs'] = [approach for approach in approaches_ser if
                                            approach['stage_id'] == child_stage['stage_id']]

        return Response(parent_stages, status=HTTP_200_OK)


class AcademicWorkForTeacherView(APIView):

    def get(self, **kwargs):
        id_teacher = kwargs.get('pk')

        academic_work = AcademicWork.objects.select_related('student_id').filter(teacher_id=id_teacher)
        academic_work_ser = AcademicWorkWithStudentSerializer(academic_work, many=True)

        return Response(academic_work_ser.data, status=HTTP_200_OK)


# class AcademicWorkForStudentView(APIView):
#
#     def get(self, **kwargs):
#         id_student = kwargs.get('pk')
#
#         academic_work = AcademicWork.objects.select_related('teacher_id').filter(student_id=id_student)
#         academic_work_ser =
#


