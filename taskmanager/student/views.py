from rest_framework.response import Response
from rest_framework.status import HTTP_200_OK, HTTP_400_BAD_REQUEST
from rest_framework.views import APIView

from .services import MainStudent
# Create your views here.


class AcademicWorks(APIView):
    def get(self, request, **kwargs):
        pk = kwargs.get('pk')
        student = MainStudent(pk)
        return Response(student.serialize_academic_work(), status=HTTP_200_OK)

