from .models import Student, AcademicWork, StudentGroup, FormOfControl

from .serializers import AcademicWorkSerializer


class MainStudent:
    def __init__(self, pk):
        self.model = Student.objects.get(user__pk=pk)
        self.academic_work = self.__find_academic_works()
        self.group = self.model.group_id

    def __find_academic_works(self):
        return AcademicWork.objects.filter(student_id=self.model.user.id)

    def serialize_academic_work(self):
        academic_work = AcademicWorkSerializer(self.academic_work, many=True)
        return academic_work.data

    def get_form_of_control(self):
        form_of_control = FormOfControl.objects.filter()


# class FormofControl:
#     def __init__(self, student):
#         self.model



