from django.urls import path
from .views import DisciplineView, FormOfControlView, \
    AcademicWorkView, AcademicWorkDetailView, AcademicWorkForTeacherView, \
    TemplateView, TemplateDetailView, ApproachView, StageView, SpecializationaView, StudentGroupView

urlpatterns = [
    path('disc/', DisciplineView.as_view(), name='disciplines list'),
    path('specializations/', SpecializationaView.as_view(), name='all specializations'),
    path('control/', FormOfControlView.as_view(), name='forms of control list'),
    path('studentgroup/', StudentGroupView.as_view(), name='all student group'),
    path('academs/', AcademicWorkView.as_view(), name='academic work list'),
    path('academs/<int:pk>/', AcademicWorkDetailView.as_view(), name='academic work detail'),
    path('academs-<int:pk>/', AcademicWorkForTeacherView.as_view(), name='academic work for teacher'),
    path('templates/<int:pk>/', TemplateView.as_view(), name='template for the teacher'),
    path('template-<int:pk>/', TemplateDetailView.as_view(), name='template`s details'),
    path('approach/', ApproachView.as_view(), name='add approach to stage'),
    path('stage/', StageView.as_view(), name='add, edit student`s stages')
]
