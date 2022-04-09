from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST, HTTP_500_INTERNAL_SERVER_ERROR
from rest_framework.views import APIView
from typing import List, Dict

from .serializers import AcademicWork, AcademicWorkSerializer, AcademicWorkWithStudentSerializer
from .serializers import Approach, ApproachSerializer
from .serializers import DisciplineSerializer, Discipline
from .serializers import FormOfControlSerializer, FormOfControl
from .serializers import SpecializationSerializer, Specialization
from .serializers import Stage, StageSerializer
from .serializers import StudentGroup, StudentGroupSerializer

from .services import get_template_by_teacher_id, create_template_name, \
    get_template_by_id, update_template_name, delete_template_name, add_stages_by_name_template,\
    MainNameTemplate, MainTeacher, MainTemplateStage, MainDiscipline, MainAcademicWork, teacher, template_detail


class StudentGroupView(APIView):
    """ Вывод всех студенческих групп """

    def get(self, request,  **kwargs):
        groups = StudentGroup.objects.all()
        serializer = StudentGroupSerializer(data=groups, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SpecializationaView(APIView):

    def get(self, request, **kwargs):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(data=specializations, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class DisciplineView(APIView):
    """ Вывод всех дисциплин по гет запросу """

    def get(self, request):
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
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
            full_name = params.get('name', None)

            academic_form = AcademicWork.objects.filter(form_of_control_id=form_of_control_id)
            academic_group = AcademicWork.objects.filter(student_id__group_id=group_id)

            academic_ser = AcademicWorkSerializer(academic_form, many=True).data
            academic_ser += AcademicWorkSerializer(academic_group, many=True).data

        else:
            academic_work = AcademicWork.objects.all()
            academic_ser = AcademicWorkSerializer(academic_work, many=True).data

        return Response(academic_ser, status=HTTP_200_OK)


class AcademicWorkDetailView(APIView):
    """
        Вывод информации по учебной работе вместе с этапами и подходами
        Объединение таблиц Подход и Этап. У каждого этапа может быть несолько под этапов.
        А у каждого подэтапа может быть несколько подходов.

        TODO Вынести логику выполнения запроса к базе данных и форировании ответа в виде JSON
    """

    def get(self, request, pk):
        academic_work = MainAcademicWork(pk)
        stages = academic_work.academ_work_detail()
        return Response(stages, status=HTTP_200_OK)


class AcademicWorkForTeacherView(APIView):
    def get(self, request,  **kwargs):
        id_teacher = kwargs.get('pk')

        teacher = MainTeacher(id_teacher)
        academ_work = teacher.get_academic_work()

        return Response(academ_work, status=HTTP_200_OK)

    def post(self):
        pass

    def put(self):
        pass

    def delete(self):
        pass


class TemplateView(APIView):
    """ Вывод всех шаблон для преподавателя по его идентификатору """
    def get(self, request, **kwargs):
        teacher_id = kwargs.get('pk')
        try:
            templates = teacher(teacher_id)
            return Response(templates, status=HTTP_200_OK)
        except:
            return Response({'message': 'Такого преподавателя нет!'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        data = request.data
        template_id = data.get('template_id')
        template = MainNameTemplate(template_id)
        template = template.update(data)
        return Response(template, status=HTTP_200_OK)

    def delete(self, request, **kwargs):
        template_id = request.data.get('template_id')
        template = MainNameTemplate(template_id)
        if template.delete():
            return Response({'message': 'Удалено успешно!'}, status=HTTP_200_OK)
        return Response({'message': 'Объект не найден'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


    def post(self, request, **kwargs):
        data = request.data
        teacher_id = kwargs.get('pk')
        try:
            MainNameTemplate.create(data)
            templates = teacher(teacher_id)
            return Response(templates, HTTP_200_OK)
        except:
            return Response({'message': 'Error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class TemplateDetailView(APIView):
    """ Вывод информации по кокретному шаблону. Добавление шаблона и изменение информации по нему """

    def get(self, request, **kwargs):
        template_id = kwargs.get('pk')
        template = MainNameTemplate(template_id)
        templates = template.get_stages()
        return Response(templates, status=HTTP_200_OK)

    def put(self, request, **kwargs):
        template_id = kwargs.get('pk')
        data = request.data
        template = update_template_name(template_id, data)
        return Response(template, status=HTTP_200_OK)

    def delete(self, request, **kwargs):
        data = request.data.get('stages_id')
        result = MainNameTemplate.delete_stages(data)
        result_data = {'result': result}
        if result:
            return Response(result_data, status=HTTP_200_OK)
        return Response(result_data, status=HTTP_400_BAD_REQUEST)


class StageTemplateView(APIView):
    """ Добавление этапов к шаблону """
    def post(self, request, **kwargs):
        template_stage_data = request.data
        template_stages = add_stages_by_name_template(template_stage_data)
        return Response(template_stages, status=HTTP_200_OK)


class CreateNameTemplateView(APIView):
    """ Добавление шаблона """
    def post(self, request, **kwargs):
        template_name = create_template_name(request.data)
        return Response(template_name)

    def put(self, request, **kwargs):
        pass
        # data = request.data
        # template_stage = update_stage_template(data)
        #
        # return Response(template_stage, status=HTTP_200_OK)


# class AcademicWorkForStudentView(APIView):
#
#     def get(self, **kwargs):
#         id_student = kwargs.get('pk')
#
#         academic_work = AcademicWork.objects.select_related('teacher_id').filter(student_id=id_student)
#         academic_work_ser =
#
