import json
from abc import ABC, abstractmethod

from typing import List, Dict

from .serializers import AcademicWork, AcademicWorkSerializer, AcademicWorkWithStudentSerializer
from .serializers import Approach, ApproachSerializer
from .serializers import DisciplineSerializer, Discipline
from .serializers import FormOfControlSerializer, FormOfControl
from .serializers import SpecializationSerializer, Specialization
from .serializers import Stage, StageSerializer
from .serializers import StudentGroup, StudentGroupSerializer
from .serializers import TemplateStageSerializer, NameTemplateStageSerializer

from .models import TemplateStage, NameTemplate, Teacher, Discipline, StudentGroup

"""

Классы

"""


class StageTemplate:
    def __init__(self, model):
        self.model = model


class TemplateName:
    def __init__(self, model):
        self.model = model
        self.name = model.name
        self.template_id = model.template_id
        self.teacher_id = model.teacher_id


class Lecturer:
    def __init__(self, model):
        self.model = model
        self.teacher_id = model.user.id




"""

    Функции

"""


def add_stages_by_name_template(template_stage_data):
    template_id = template_stage_data[0]['template_id']

    for template in template_stage_data:
        if template['childs']:
            parent_template = TemplateStageSerializer(data=template)
            if parent_template.is_valid():
                parent_template.save()
                pk = parent_template.data['stage_id']
                for child in template['childs']:
                    child['parent_id'] = pk
                    template_ser = TemplateStageSerializer(data=child)
                    if template_ser.is_valid():
                        template_ser.save()
        else:
            template_ser = TemplateStageSerializer(data=template)
            if template_ser.is_valid():
                template_ser.save()

    templates = get_template_by_id(template_id)
    return templates


def delete_template_name(template_id: int):
    try:
        template_name = NameTemplate.objects.get(template_id=template_id)
        template_name.delete()
        return True
    except:
        return False


def update_template_name(template_id: int, data: List[Dict]):
    template_name = NameTemplate.objects.get(template_id=template_id)
    template_name_ser = NameTemplateStageSerializer(instance=template_name, data=data)

    if template_name_ser.is_valid():
        template_name_ser.save()
    print(template_name_ser.data)
    return template_name_ser.data


def create_template_name(data: List[Dict]) -> NameTemplateStageSerializer:
    """ Создание шаблона работы. """
    template_name = NameTemplateStageSerializer(data=data)
    if template_name.is_valid():
        template_name.save()
    return template_name.data


def get_template_by_id(template_id: int):
    """
        Функция возвращающая информацию по шаблону с переданным идентификатором

        template_id: id шаблона, информацию по которому нужно вернуть
    """

    template_name = NameTemplate.objects.get(template_id=template_id)
    template_stages = TemplateStage.objects.filter(template_id=template_id)

    template_stages_ser = TemplateStageSerializer(template_stages, many=True).data
    template_names_ser = NameTemplateStageSerializer(template_name).data

    parent_template = [template for template in template_stages_ser if template['parent_id'] is None]
    child_templates = [template for template in template_stages_ser if not template['parent_id'] is None]

    for template in parent_template:
        template['childs'] = [child_template for child_template in child_templates
                              if child_template['parent_id'] == template['stage_id']]

    template_names_ser['stages'] = parent_template

    return template_names_ser


def get_template_by_teacher_id(teacher_id: int) -> List[Dict]:
    """
         Функция возвращает шаблоны этапов по id преподавателя в виде списка словарей

         teacher_id - идентификатор преподавателя
    """

    template_names = NameTemplate.objects.filter(teacher_id=teacher_id)
    template_names_ser = NameTemplateStageSerializer(template_names, many=True).data

    return template_names_ser


def academic_work_detail_by_id(academ_id: int) -> List[Stage]:
    def get_approach_id(approaches: List[Dict], stage_id: int) -> List[Dict]:
        """
            Функция для генерации списка подходов по id этапа.

            approaches - общий список подходов
            stage_id  - id этапа
        """
        return [approach for approach in approaches if approach['stage_id'] == stage_id]

    def union_parent_and_child_stages(parent_stages: List[Dict], child_stages: List[Dict]):
        for stage in parent_stages:
            stage['child'] = [child_stage for child_stage in child_stages if
                              stage['stage_id'] == child_stage['parent_stage_id']]

    def add_approach_in_stage(stages: List[Dict], approaches: List[Dict]) -> None:
        for stage in stages:
            if stage['child']:
                for child_stage in stage['child']:
                    child_stage['apporaches'] = get_approach_id(approaches, child_stage['stage_id'])
            else:
                stage['apporaches'] = get_approach_id(approaches, stage['stage_id'])

    stages = Stage.objects.filter(academic_work_id=academ_id)
    approaches = Approach.objects.filter(stage_id__in=stages)

    stages_ser = StageSerializer(stages, many=True).data
    approaches_ser = ApproachSerializer(approaches, many=True).data

    parent_stages = [stage for stage in stages_ser if stage['parent_stage_id'] is None]
    child_stages = [stage for stage in stages_ser if not stage['parent_stage_id'] is None]

    union_parent_and_child_stages(parent_stages, child_stages)
    add_approach_in_stage(parent_stages, approaches_ser)

    return parent_stages
