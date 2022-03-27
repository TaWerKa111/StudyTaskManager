from django.urls import path
from .views import AcademicWorks

urlpatterns = [
    path('academs/<int:pk>', AcademicWorks.as_view(), name='student`s works'),
]
