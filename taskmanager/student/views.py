from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .services import MainStudent, select_academic_works
# Create your views here.


class AcademicWorksView(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        student = MainStudent(pk)
        return Response(student.serialize_academic_work(), status=HTTP_200_OK)

    def post(self, request, **kwargs):
        data = request.data
        params = data.get('params')
        academs = data.get('academs')

        if params:
            academic_ser = select_academic_works(academs, params)
        else:
            academic_ser = request.data

        return Response(academic_ser, status=HTTP_200_OK)


class AcademicDetails(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        pass


""""
{
    "params": {},
    "academs": [
            {
                "academic_work_id": 4,
                "name": "Dip",
                "is_complited": false,
                "student_id": 3,
                "discipline_id": 1,
                "form_of_control_id": 2,
                "teacher_id": 1
            }
        ]
}
"""