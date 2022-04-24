from abc import ABC, abstractmethod
from typing import List, Dict

from .serializers import (
    AcademicWork,
    AcademicWorkSerializer,
    AcademicWorkWithStudentSerializer,
)
from .serializers import Approach, ApproachSerializer
from .serializers import DisciplineSerializer, Discipline
from .serializers import FormOfControlSerializer, FormOfControl
from .serializers import SpecializationSerializer, Specialization
from .serializers import Stage, StageSerializer
from .serializers import StudentGroup, StudentGroupSerializer
from .serializers import TemplateStageSerializer, NameTemplateStageSerializer, Student

from .models import TemplateStage, NameTemplate, Teacher, Discipline, StudentGroup

"""

Классы

"""


class Receiver(ABC):

    """
    Абстрактный класс, который выполняет действия в команде.

    Методы:
        - create: создание объектов в бд
        - update: обновление объектов в бд
        - delete: удаление объектов из бд
    """

    @abstractmethod
    def create(self, data):
        pass

    @abstractmethod
    def update(self, data):
        pass

    @abstractmethod
    def delete(self):
        pass


class MainTemplateStage:
    """
    Этап шаблона.

    Атрибуты:
        - model TemplateStage: моделька этапа шаблона
    """
    def __init__(self, model):
        self.model = model


class MainNameTemplate(Receiver):
    """
    Шаблон работы.

    Атрибуты:
        - pk int: первичный ключ
        - model NameTemplate: моделька этапа
        - name str: название шаблона

    Методы:
        - __create_model_with_pk: создание, получение данных по шаблону из бд
        - delete: удаление шаблона из бд, с ним удаляются все этапы
        - update: обновление данных по шаблону
        - create: создание шаблона
        - get_stages: получение этапов по конкретному шаблону
        - delete_stages: удаление этапов из шаблона
        - __add_with_child: добавление этапа с потомками
        - __add_with_no_child: добавление этапа без потомков
        - add_stages: добавление этапов
        - update_stages: обновление этапов
    """
    def __init__(self, template_id: int = None):
        if template_id:
            try:
                self.pk = template_id
                self.__create_model_with_pk()
            except Exception:
                raise Exception('Нет такой записи!')

    def __create_model_with_pk(self):
        if self.pk:
            self.model = NameTemplate.objects.get(template_id=self.pk)
            self.name = self.model.name
            self.template_id = self.model.template_id
            self.stages = []

    def delete(self):
        """
        Удаление шаблона.
        True если шаблона удален, иначе False.

        :return bool: возвращает результат удаления шаблона
        """
        try:
            template_name = NameTemplate.objects.get(template_id=self.template_id)
            template_name.delete()
            return True
        except Exception:
            return False

    def update(self, data):
        """
        Обновление шаблона
        Результат = True, если данные шаблона изменены, иначе False

        :return bool: результат обновления шаблона
        """
        template_name_ser = NameTemplateStageSerializer(instance=self.model, data=data)

        if template_name_ser.is_valid():
            template_name_ser.save()
            return True
        return False

    @classmethod
    def create(cls, data):
        """
        Создание шаблона.
        Результат = True, если шаблона добавлен, иначе False.

        :return bool: результат создания шаблона
        """
        template_name = NameTemplateStageSerializer(data=data)
        if template_name.is_valid():
            template_name.save()
            return True
        return False

    def get_stages(self):
        """
        Функция возвращающая информацию по шаблону с переданным идентификатором
        """

        template_name = NameTemplate.objects.get(template_id=self.pk)
        template_stages = TemplateStage.objects.filter(template_id=self.pk)

        template_stages_ser = TemplateStageSerializer(template_stages, many=True).data
        template_names_ser = NameTemplateStageSerializer(template_name).data

        parent_template = [
            template
            for template in template_stages_ser
            if template["parent_id"] is None
        ]
        child_templates = [
            template
            for template in template_stages_ser
            if not template["parent_id"] is None
        ]

        for template in parent_template:
            template["childs"] = [
                child_template
                for child_template in child_templates
                if child_template["parent_id"] == template["stage_id"]
            ]

        template_names_ser["stages"] = parent_template

        return template_names_ser

    @classmethod
    def delete_stages(cls, pk_list):
        """
        Удаление этапов шаблона.
        """
        try:
            stages = TemplateStage.objects.filter(stage_id__in=pk_list)
            stages.delete()
            return True
        except:
            return False

    def __add_with_child(self, stage, instances: dict = None):
        instance_par = instances.get(stage['stage_id'], 'None')
        parent_template = TemplateStageSerializer(data=stage, instance=instance_par)
        if parent_template.is_valid():
            parent_template.save()
            pk = parent_template.data["stage_id"]
            for child in stage["childs"]:
                child["parent_id"] = pk
                instance_child = instances.get(child['stage_id'], None)
                self.__add_with_no_child(child, instance=instance_child)

    def __add_with_no_child(self, stage, instance=None):
        template_ser = TemplateStageSerializer(data=stage, instance=instance)
        if template_ser.is_valid():
            template_ser.save()

    def add_stages(self, template_stage_data):
        """
        Добавление этапов.
        """
        template_id = template_stage_data[0]["template_id"]

        for stage in template_stage_data:
            if not stage.get('stage_id', None):
                if stage.get("childs", None):
                    self.__add_with_child(stage)
                else:
                    self.__add_with_no_child(stage)
            for child in stage.get("childs", None):
                if not child.get('stage_id', None):
                    child["parent_id"] = stage['stage_id']
                    self.__add_with_no_child(child)

    def update_stages(self, template_stage_data):
        """
        Обновление данных этапов у шаблона.
        """
        instances = dict()

        for stage in template_stage_data:
            instances[stage['stage_id']] = TemplateStage.objects.get(stage_id=stage['stage_id'])
            if stage['childs']:
                for child in stage['childs']:
                    instances[child['stage_id']] = TemplateStage.objects.get(stage_id=child['stage_id'])

        for stage in template_stage_data:
            if stage["childs"]:
                self.__add_with_child(stage, instances=instances)
            else:
                self.__add_with_no_child(stage, instance=instances[stage['stage_id']])


class MainDiscipline:
    def __init__(self, model):
        self.model = model


class MainTeacher:
    """
    Декорирует класс Преподаватель.

    Атрибуты:
        - model Teacher: объект класс Teacher

    Методы:
        - get_template list: получение списка шаблонов для преподавателя.
        - get_academic_work list: получение академических работ для преподавателя.
    """
    def __init__(self, teacher_id: int):
        self.model = Teacher.objects.get(pk=teacher_id)

    def get_template(self):
        """
        Функция возвращает шаблоны этапов по id преподавателя в виде списка словарей

        :return List[Dict]: список шаблонов для преподавателя.
        Пример:
            [
                {
                    "template_id": int,
                    "name": str,
                    "teacher_id": int
                }
            ]
        """

        template_names = NameTemplate.objects.filter(teacher_id=self.model.pk)
        template_names_ser = NameTemplateStageSerializer(template_names, many=True).data

        return template_names_ser

    def get_academic_work(self):
        """
        Получение академических работ для преподавателя.

        :return List[Dict]: академические работы для преподавателя.
        """
        academic_work = AcademicWork.objects.select_related("student_id").filter(
            teacher_id=self.model.pk
        )
        academic_work_ser = AcademicWorkWithStudentSerializer(
            academic_work, many=True
        ).data
        return academic_work_ser


class MainStage:
    """
    Этап. Часть сдачи работы. Т.е. работа разбивается на этапы.

    Методы:
        - delete: удаление этапа
        - update: обновление данных этапа
        - create: создание этапа


    """
    def __init__(self, stage_id):
        self.model = Stage.objects.get(stage_id=stage_id)

    def delete(self) -> bool:
        """
        Удаление этапа.

        :return bool: True, если этап удален, иначе False.
        """
        try:
            self.model.delete()
            return True
        except Exception:
            return False

    def update(self, stage_data: Dict) -> bool:
        """
        Обновление данных по шаблону.

        :return bool: True, если данные по этапу изменены, иначе False
        """
        stage_data_ser = StageSerializer(instance=self.model, data=stage_data)

        if stage_data_ser.is_valid():
            stage_data_ser.save()
            return True
        return False

    @classmethod
    def create(cls, academic_work, stage, parent=None) -> Dict:
        """
        Создание этапа.

        :return Dict: Данные по созданному этапу.
        """
        new_stage = Stage()
        if parent:
            new_stage.parent_stage_id = parent
        new_stage.academic_work_id = academic_work
        new_stage.name = stage['name']
        new_stage.save()
        return new_stage


class MainAcademicWork:
    def __init__(self, academ_id: int):
        self.model = AcademicWork.objects.get(academic_work_id=academ_id)

    def academ_work_detail(self) -> List[Stage]:
        def get_approach_id(approaches: List[Dict], stage_id: int) -> List[Dict]:
            """
            Функция для генерации списка подходов по id этапа.

            approaches - общий список подходов
            stage_id  - id этапа
            """
            return [
                approach for approach in approaches if approach["stage_id"] == stage_id
            ]

        def union_parent_and_child_stages(
            parent_stages: List[Dict], child_stages: List[Dict]
        ):
            for stage in parent_stages:
                stage["child"] = [
                    child_stage
                    for child_stage in child_stages
                    if stage["stage_id"] == child_stage["parent_stage_id"]
                ]

        def add_approach_in_stage(stages: List[Dict], approaches: List[Dict]) -> None:
            for stage in stages:
                if stage["child"]:
                    for child_stage in stage["child"]:
                        child_stage["apporaches"] = get_approach_id(
                            approaches, child_stage["stage_id"]
                        )
                else:
                    stage["apporaches"] = get_approach_id(approaches, stage["stage_id"])

        stages = Stage.objects.filter(academic_work_id=self.model.academic_work_id)
        approaches = Approach.objects.filter(stage_id__in=stages)

        stages_ser = StageSerializer(stages, many=True).data
        approaches_ser = ApproachSerializer(approaches, many=True).data

        parent_stages = [
            stage for stage in stages_ser if stage["parent_stage_id"] is None
        ]
        child_stages = [
            stage for stage in stages_ser if not stage["parent_stage_id"] is None
        ]

        union_parent_and_child_stages(parent_stages, child_stages)
        add_approach_in_stage(parent_stages, approaches_ser)

        return parent_stages

    @classmethod
    def add_stages_to_student(cls, academic_work, template_stages: dict):
        for stage in template_stages:
            parent = MainStage.create(academic_work, stage)
            if stage.get('childs', None):
                for child_stage in stage.get('childs'):
                    MainStage.create(academic_work, child_stage, parent)

    @classmethod
    def create(cls, form_control, discipline, student, teacher, template_stages: dict):
        academ_work = AcademicWork()
        academ_work.name = f'{student} {form_control.name}'
        academ_work.student_id = student
        academ_work.discipline_id = discipline
        academ_work.form_of_control_id = form_control
        academ_work.teacher_id = teacher
        academ_work.save()

        cls.add_stages_to_student(academic_work=academ_work, template_stages=template_stages)


class MainApproach(Receiver):
    """
    Класс подхода. Студент может сдавать работу по этапу в несколько подходов.

    Атрибуты:
        - model Approach: объект класса Подход

    Методы:
        - update: изменение данных подхода
        - delete: удаление подхода
        - create: создание подхода
        - delete: удаление подхода
    """
    def __init__(self, approach_id):
        self.model = Approach.objects.get(approach_id=approach_id)

    def update(self, data: Dict) -> bool:
        """
        Обновление данных подхода.

        Параметры:
            - :param data: новые данные по подходу (название, id, id этапа, коммент)

        :return bool: True, если этап изменен, иначе False
        """
        approach_ser = ApproachSerializer(data=data, instance=self.model)
        if approach_ser.is_valid():
            approach_ser.save()
            return True
        return False

    @classmethod
    def create(cls, data: List[Dict]) -> bool:
        """
        Создание подхода.

        Параметры:
            - :param data: данные по подходу (имя, id этапа, название, коммент)

        :return bool: True, если подход создан, иначе False
        """
        approach_ser = ApproachSerializer(data=data)
        if approach_ser.is_valid():
            approach_ser.save()
            return True
        return False

    def delete(self) -> bool:
        """
        Удаление подхода.

        :return bool: True, если подход удален, иначе False
        """
        try:
            self.model.delete()
            return True
        except:
            return False


"""

    Функции

"""


def get_template(teacher_id: int) -> List[Dict]:
    """
    Получение шаблонов по идентификатору преподавателя.

    :param teacher_id: int  идентификатора преподавателя.
    """
    teacher = MainTeacher(teacher_id)
    templates = teacher.get_template()
    return templates


def template_detail(template_id: int) -> List[Dict]:
    """
    Получение данных по определенному шаблону.

    Параметры:
        - :param template_id: int идентификатор шаблона
    """
    template = MainNameTemplate(template_id)
    templates = template.get_stages()
    return templates


def create_or_update_template_stages(template_id: int, data: dict, method) -> List[Dict]:
    """
    Создание или изменение этапов шаблона.

    Если метод = post: происходит создание этапов шаблона
    Иначе: происходит изменение этапов шаблона.

    :return: список этапов шаблона.
    """
    template = MainNameTemplate(template_id)

    if method == 'post':
        template.add_stages(data['stages'])
    else:
        template.update_stages(data['stages'])

    template_info = template.get_stages()
    return template_info


def create_academic_work(teacher: MainTeacher, data: Dict) -> bool:
    """
    Создание академической работы по шаблону для определенной группы студентов.

    Атрибуты:
        - group_id int: идентификатор группы студентов
        - form_control_id int: идентификатор формы контроля
        - template_id int: идентификатор шаблона
        - discipline_id int: идентификатор дисциплины

    :return: bool
    """
    group_id = data.get('group_id', None)
    form_control_id = data.get('form_control_id', None)
    template_id = data.get('template_id', None)
    discipline_id = data.get('discipline_id', None)

    if group_id and form_control_id and template_id:
        students = Student.objects.filter(group_id=group_id)
        template = MainNameTemplate(template_id=template_id)
        template_stages = template.get_stages()
        form_control = FormOfControl.objects.get(form_of_control_id=form_control_id)
        discipline = Discipline.objects.get(discipline_id=discipline_id)

        for student in students:
            MainAcademicWork.create(form_control, discipline, student, teacher, template_stages['stages'])

        return True
    return False

