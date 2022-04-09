from django.urls import path
from .views import DisciplineView, FormOfControlView, \
    AcademicWorkView, AcademicWorkDetailView, AcademicWorkForTeacherView, \
    TemplateView, CreateNameTemplateView, TemplateDetailView, StageTemplateView

urlpatterns = [
    path('disc/', DisciplineView.as_view(), name='disciplines list'),
    path('control/', FormOfControlView.as_view(), name='forms of control list'),
    path('academs/', AcademicWorkView.as_view(), name='academic work list'),
    path('academs/<int:pk>', AcademicWorkDetailView.as_view(), name='academic work detail'),
    path('academs-<int:pk>', AcademicWorkForTeacherView.as_view(), name='academic work for teacher'),
    path('templates/<int:pk>', TemplateView.as_view(), name='template for the teacher'),
    path('create-template/', CreateNameTemplateView.as_view(), name='create template'),
    path('template-<int:pk>', TemplateDetailView.as_view(), name='template`s details'),
    path('template/stage/add', StageTemplateView.as_view(), name='work with stages'),
]
