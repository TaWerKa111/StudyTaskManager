from .models import Student, AcademicWork, StudentGroup, FormOfControl

from .serializers import AcademicWorkSerializer, FormOfControlSerializer


class MainAcademicWork:
    def __init__(self):
        pass


class MainStudent:
    """
         Класс студента декорирует класс Student.

         self.model - экземпляр класс Student
         self.academic_work - академические работы студента
         self.group - група студента
    """

    def __init__(self, pk, academic_work=None):
        self.model = Student.objects.get(user__pk=pk)
        self.group = self.model.group_id
        self.form_of_control = self.get_form_of_control()
        self.academic_work = self.__find_academic_works()

    def __find_academic_works(self):
        """ Поиск работу для студента """
        return AcademicWork.objects.filter(student_id=self.model.user.id)

    def serialize_academic_work(self):
        """ Сериализация работ для дельнейшей передачи клиенту """
        academic_work = AcademicWorkSerializer(self.academic_work, many=True)
        return academic_work.data

    def serialize_form_of_control(self):
        form_of_control_ser = FormOfControlSerializer(data=self.form_of_control, many=True)
        return form_of_control_ser

    def get_form_of_control(self):
        return FormOfControl.objects.all()


class AcademicWorks:
    def __init__(self, data):
        self.academics = AcademicWorkSerializer(data=data, many=True)

    def select_academic_work(self, name=None, work_id=None, discipline_id=None, is_complited=False):

        if self.academics.is_valid():
            selected_academics = [academic_work for academic_work in self.academics.data
                                  if (name and name in academic_work['name'])
                                  or (work_id and work_id == academic_work['form_of_control_id'])
                                  or (discipline_id and academic_work['discipline_id'])
                                  or (academic_work['is_complited'] == is_complited)]

            selected_academics_ser = AcademicWorkSerializer(selected_academics, many=True)

            return selected_academics

        return None


def select_academic_works(data,  params):
    Academic_works = AcademicWorks(data)
    name = params.get('name', None)
    work_id = params.get('work_id', None)
    discipline_id = params.get('discipline_id', None)
    is_complited = params.get('is_complited', False)

    academic_works = Academic_works.select_academic_work(name=name, work_id=work_id,
                                                         discipline_id=discipline_id, is_complited=is_complited)
    return academic_works

