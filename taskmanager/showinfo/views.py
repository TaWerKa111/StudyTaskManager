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

from .services import  MainNameTemplate, MainTeacher, MainTemplateStage, \
    MainDiscipline, MainAcademicWork, get_template, \
    template_detail, create_or_update_template_stages, create_academic_work, MainApproach, MainStage

from .commands import AddCommand, UpdateCommand, DeleteCommand, Invoker


class StudentGroupView(APIView):
    """
    Вывод всех студенческих групп

    Методы:
        - get: принятие гет запроса (отправка списка групп в виде JSON).

    Пример:
        [
            {
                "group_id": 1,
                "name": "IST-19",
                "specialization_id": 1
            }
        ]
    """

    def get(self, request,  **kwargs):
        groups = StudentGroup.objects.all()
        serializer = StudentGroupSerializer(groups, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class SpecializationaView(APIView):
    """
    Вывод всех Специальностей

    Методы:
        - get: принятие гет запроса (отправка списка групп в виде JSON).

    Пример:
        [
            {
                "specialization_id": 1,
                "name": "IST"
            }
        ]
    """
    def get(self, request, **kwargs):
        specializations = Specialization.objects.all()
        serializer = SpecializationSerializer(specializations, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class DisciplineView(APIView):
    """
    Вывод всех дисциплин

    Методы:
        - get: принятие гет запроса (отправка списка групп в виде JSON).

    Пример:
        [
            {
                "discipline_id": 1,
                "name": "Базы данных"
            }
        ]
    """

    def get(self, request):
        disciplines = Discipline.objects.all()
        serializer = DisciplineSerializer(disciplines, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class FormOfControlView(APIView):
    """
    Вывод всех форм контроля (ргр, курсовые и т.д.)

    Методы:
        - get: принятие гет запроса (отправка списка групп в виде JSON).

    Пример:
        [
            {
                "form_of_control_id": 1,
                "name": "RGR"
            }
        ]
    """
    def get(self, request):
        form_of_control = FormOfControl.objects.all()
        serializer = FormOfControlSerializer(form_of_control, many=True)
        return Response(serializer.data, status=HTTP_200_OK)


class AcademicWorkView(APIView):
    """
    Вывод всех академических работ.

    Методы:
        - get: принятие гет запроса (отправка списка групп в виде JSON).

    Пример вывода:
        [
            {
                "academic_work_id": 10,
                "name": "Егор Егоров RGR",
                "is_complited": false,
                "student_id": 2,
                "discipline_id": 1,
                "form_of_control_id": 1,
                "teacher_id": 1
            },
            {
                "academic_work_id": 11,
                "name": "Егорова Лиана RGR",
                "is_complited": false,
                "student_id": 3,
                "discipline_id": 1,
                "form_of_control_id": 1,
                "teacher_id": 1
            }
        ]
    """
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
    Вывод информации по учебной работе вместе с этапами и подходами.

    Объединение таблиц Подход и Этап. У каждого этапа может быть несколько под этапов.
    А у каждого подэтапа может быть несколько подходов.

    Методы:
        - get: принятие гет запроса (отправка списка групп в виде JSON).

    Пример:
        [
            {
                "stage_id": 10,
                "name": "Подготовка",
                "is_pass": false,
                "planned_date": "2022-04-10",
                "actually_date": "2022-04-10",
                "academic_work_id": 10,
                "parent_stage_id": null,
                "child": [
                    {
                        "stage_id": 11,
                        "name": "Описание предметной области",
                        "is_pass": true,
                        "planned_date": "2022-04-10",
                        "actually_date": "2022-04-10",
                        "academic_work_id": 10,
                        "parent_stage_id": 10,
                        "apporaches": [
                            {
                                "approach_id": 3,
                                "name": "Показал описание предметной области",
                                "comment": "Доделать таблицу",
                                "date": "2022-04-10",
                                "stage_id": 11
                            }
                        ]
                    },
                    {
                        "stage_id": 16,
                        "name": "Описание схем",
                        "is_pass": false,
                        "planned_date": "2022-04-16",
                        "actually_date": "2022-04-16",
                        "academic_work_id": 10,
                        "parent_stage_id": 10,
                        "apporaches": []
                    }
                ]
            }
        ]
    """

    def get(self, request, pk):
        try:
            academic_work = MainAcademicWork(pk)
            stages = academic_work.academ_work_detail()
            return Response(stages, status=HTTP_200_OK)
        except:
            return Response({'result': False, 'message': 'Нет академической работы!'})


class AcademicWorkForTeacherView(APIView):
    """
    Работы академических студентов для определенного преподавателя.
    Идентификатор преподавателя передается в строке запроса после дефиса.

    Методы:
        - get: принятие гет запроса (отправка списка групп в виде JSON).
        - post: создание академической работы по шаблону работы.
        - delete: удаление академической работы или работ.

    Пример:
        [
            {
                "academic_work_id": 10,
                "student_id": {
                    "id": 2,
                    "num_z": "992322",
                    "user": 3,
                    "group_id": 1
                },
                "name": "Егор Егоров RGR",
                "is_complited": false,
                "discipline_id": 1,
                "form_of_control_id": 1,
                "teacher_id": 1
            },
            {
                "academic_work_id": 11,
                "student_id": {
                    "id": 3,
                    "num_z": "191404",
                    "user": 4,
                    "group_id": 1
                },
                "name": "Егорова Лиана RGR",
                "is_complited": false,
                "discipline_id": 1,
                "form_of_control_id": 1,
                "teacher_id": 1
            }
        ]
    """
    def get(self, request,  **kwargs):
        """
        Получение работ студентов по идентификатору преподавателя.
        """
        id_teacher = kwargs.get('pk')
        try:
            teacher = MainTeacher(id_teacher)
            academ_work = teacher.get_academic_work()

            return Response(academ_work, status=HTTP_200_OK)
        except:
            return Response({'result': False, 'message': 'Такого преподавателя нет!'}, status=HTTP_200_OK)

    def post(self, request, **kwargs):
        """
        Создание академической работы для группы студентов. По определенному шаблону.

        Пример запроса:
            {
                "group_id": 1,         pk группы студентов, для которой применяется шаблон.
                "form_control_id": 1,  форма контроля для академической работы
                "template_id": 1,      pk шаблона, по которому происходит удаление
                "discipline_id": 1     pk дисциплины
            }
        """
        try:
            id_teacher = kwargs.get('pk')
            data = request.data
            teacher = MainTeacher(id_teacher)
            create_academic_work(teacher.model, data)
            academ_work = teacher.get_academic_work()

            return Response(academ_work, status=HTTP_200_OK)
        except:
            return Response({'result': False, 'message': 'Такого преподавателя нет!'}, status=HTTP_200_OK)

    def put(self):
        pass

    def delete(self):
        pass


class TemplateView(APIView):
    """
    Вывод всех шаблон для преподавателя по его идентификатору

    Методы:
        - get: получение всех шаблонов
        - post: создание шаблонов для преподавателя
        - delete: удаление шаблона
        - put: обновление шаблона

    Примеры:
        Находятся в каждом методе.
    """

    def get(self, request, **kwargs):
        """
        Получение всех шаблонов по идентификатору преподавателя.

        Атрибуты:
            - teacher_id: идентификатор преподавателя, передается в теле запроса.
            - templates: список шаблонов в виде JSON.

        Пример:
            [
                {
                    "template_id": 1,
                    "name": "Курсовая",
                    "teacher_id": 1
                },
                {
                    "template_id": 3,
                    "name": "РГР",
                    "teacher_id": 1
                }
            ]
        """
        teacher_id = kwargs.get('pk')
        try:
            templates = get_template(teacher_id)
            return Response(templates, status=HTTP_200_OK)
        except:
            return Response({'message': 'Такого преподавателя нет!'}, status=HTTP_400_BAD_REQUEST)

    def put(self, request, **kwargs):
        """
        Обновление шаблона по идентификатору преподавателя.

        Атрибуты:
            - data: обновленные данные шаблона в виде JSON. Содержит поля (template_id, name, teacher_id).
            - template_id: идентификатор шаблона.
            - template: объект класса MainNameTemplate

        Пример запроса :
        {
            "template_id": 1,
            "name": "Практика",
            "teacher_id": 1
        }

        Пример Ответа - Данные обновлены:
        [
            {
                "template_id": 1,
                "name": "Практика",
                "teacher_id": 1
            },
            {
                "template_id": 3,
                "name": "РГР",
                "teacher_id": 1
            }
        ]
         """
        data = request.data
        template_id = data.get('template_id')
        try:
            template = MainNameTemplate(template_id)
            invoker = Invoker(UpdateCommand(template, data))
            invoker.invoke()
            return Response({'message:': True}, status=HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.__str__()}, status=HTTP_200_OK)

    def delete(self, request, **kwargs):
        """
        Удаление шаблона.

        Атрибуты:
            - template_id: идентификатор шаблона.
            - template: объект класса MainNameTemplate

        Пример:
            {
                "template_id": 4,
                "name": "Диплом",
                "teacher_id": 1
            }

        Пример ответа:
            Если шаблон существовал:
                {"message": "Удалено успешно!"}
            Иначе:
                {"message": "Объект не найден"}
        """
        template_id = request.data.get('template_id')
        try:
            invoker = Invoker(DeleteCommand(MainNameTemplate(template_id)))
            invoker.invoke()
            return Response({'message': 'Удалено успешно!'}, status=HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.__str__()}, status=HTTP_500_INTERNAL_SERVER_ERROR)

    def post(self, request, **kwargs):
        """
        Создание шаблона.

        Пример запроса:
            {
                "name": "Диплом",
                "teacher_id": 1
            }

        Пример ответа:
            [
                {
                    "template_id": 1,
                    "name": "Практика",
                    "teacher_id": 1
                },
                {
                    "template_id": 3,
                    "name": "РГР",
                    "teacher_id": 1
                },
                {
                    "template_id": 4,
                    "name": "Диплом",
                    "teacher_id": 1
                }
            ]
        """
        data = request.data
        teacher_id = kwargs.get('pk')
        try:
            # Выполнение команды на добавление данных в БД
            create_command = AddCommand(MainNameTemplate, data)
            invoker = Invoker(create_command)
            invoker.invoke()

            templates = get_template(teacher_id)
            return Response(templates, HTTP_200_OK)
        except:
            return Response({'message': 'Error'}, status=HTTP_500_INTERNAL_SERVER_ERROR)


class TemplateDetailView(APIView):
    """
    Вывод информации по кокретному шаблону. Добавление шаблона и изменение информации по нему

    Методы:
        - get: получение информации по конкретному шаблону (этапы)
        - put: изменение информации по шаблону.
        - delete: удаление этапов из шаблона
        - post: создание этапов шаблона
    """

    def get(self, request, **kwargs):
        """
        Получение информации по конкретному шаблону.

        Атрибуты:
            - template_id: идентификатор для шаблона.
            - template: объект класса MainNameTemplate

        Пример:
            {
                "template_id": 1,
                "name": "Практика",
                "teacher_id": 1,
                "stages": [
                    {
                        "stage_id": 1,
                        "name": "Подготовка",
                        "duration": 30,
                        "parent_id": null,
                        "template_id": 1,
                        "childs": [
                            {
                                "stage_id": 3,
                                "name": "Описание предметной области",
                                "duration": 15,
                                "parent_id": 1,
                                "template_id": 1
                            }
                        ]
                    }
                ]
            }
        """
        template_id = kwargs.get('pk')
        template = MainNameTemplate(template_id)
        templates = template.get_stages()
        return Response(templates, status=HTTP_200_OK)

    def put(self, request, **kwargs):
        """
        Обновление данные определенного этапа шаблона.

        Атрибуты:
            - template_id: идентификатор шаблона.
            - data: данные для создания этапа шаблона
                Содержат поля: template_id, name, duration, parent_id
        """
        template_id = kwargs.get('pk')
        data = request.data
        template_info = create_or_update_template_stages(template_id, data, 'put')
        return Response(template_info, status=HTTP_200_OK)

    def delete(self, request, **kwargs):
        """
        Удаление этапов для определенного шаблона.

        Атрибуты:
            - data: список, содержащий идентификаторы этапов, которые нужно удалить.
            - result: результат удаление этапов.

        Пример запроса:
            {
                "stages_id": [2, 4]
            }
        """
        data = request.data.get('stages_id')
        result = MainNameTemplate.delete_stages(data)
        result_data = {'result': result}
        if result:
            return Response(result_data, status=HTTP_200_OK)
        return Response(result_data, status=HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):
        """
        Создание этапов для определенного шаблона.

        Атрибуты:
            - template_id: идентификатор шаблона.
            - data: данные для создания этапа шаблона
                Содержат поля: template_id, name, duration, parent_id
        """
        template_id = kwargs.get('pk')
        data = request.data
        template_info = create_or_update_template_stages(template_id, data, 'post')
        return Response(template_info, status=HTTP_200_OK)


class ApproachView(APIView):
    """
    Вьюшка для работы с подходами.

    Методы:
        - post: создание подхода
        - delete: удаление подхода
        - put: изменение подхода
    """

    def post(self, request, **kwargs):
        """
        Создание подхода.

        Атрибуты:
            - data: информация для создания шаблонов.
                Поля:
                    stage_id (идентификатор этапа),
                    name (название подхода)
                    comment (комментарий по сдаче подхода)
            - result: результат создания шаблонов.

        Пример:

        """
        data = request.data
        try:
            invoker = Invoker(AddCommand(MainApproach, data))
            invoker.invoke()
            return Response({'result': True}, status=HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.__str__()}, status=HTTP_200_OK)

    def put(self, request, **kwargs):
        """
        Изменение данных по подходу.

        Атрибуты:
            - data: новые данные подхода
                 Поля:
                    stage_id (идентификатор этапа),
                    name (название подхода)
                    comment (комментарий по сдаче подхода)
            -result: результат изменения данных
        """
        data = request.data
        try:
            approach = MainApproach(data['approach_id'])
            invoker = Invoker(UpdateCommand(approach, data))
            invoker.invoke()
            return Response({'result': True}, status=HTTP_200_OK)
        except Exception as ex:
            return Response({'message': ex.__str__()}, status=HTTP_200_OK)

    def delete(self, request, **kwargs):
        """
        Удаление подхода.

        Атрибуты:
            - data: данные подхода для удаления
            - approach: объект класса MainApproach
            - result: результат удаления подхода.
        """
        try:
            data = request.data
            approach = MainApproach(data['approach_id'])
            invoker = Invoker(DeleteCommand(approach))
            invoker.invoke()
            return Response({'result': True}, status=HTTP_200_OK)
        except Exception as ex:
            return Response({'message': False}, status=HTTP_200_OK)


class StageView(APIView):
    """
    Взаимодействие с этапами конкретных студентов.
    Добавление, удаление, изменение этапов для студентов.

    Только преподаватель может выполнять все описание действия выше.
    """

    def post(self, request, **kwargs):
        stage_data = request.data
        academic_work_id = stage_data.get('academic_work_id')
        academic_work = MainAcademicWork(academic_work_id)

        parent_stage_id = stage_data.get('parent_stage_id')
        parent_stage = None

        if parent_stage_id:
            parent_stage = MainStage(stage_id=parent_stage_id).model

        MainStage.create(academic_work.model, stage_data, parent_stage)

        return Response({'result': "True"}, status=HTTP_200_OK)

    def delete(self, request, **kwargs):
        stage_data = request.data
        try:
            stage = MainStage(stage_data.get('stage_id'))
            result = stage.delete()
            if result:
                return Response({"result": "Этап успешно удален!"}, status=HTTP_200_OK)
            return Response({"result": "Этап не удален"}, status=HTTP_200_OK)
        except:
            return Response({"result": "Этап не найден"}, status=HTTP_200_OK)

    def put(self, request, **kwargs):
        stage_data = request.data
        try:
            stage = MainStage(stage_data.get('stage_id'))
            result = stage.update(stage_data)
            if result:
                return Response({"result": "Этап успешно обновлен!"}, status=HTTP_200_OK)
            return Response({"result": "Этап не обновлен!"}, status=HTTP_200_OK)
        except:
            return Response({"result": "Этап не найден"}, status=HTTP_200_OK)
