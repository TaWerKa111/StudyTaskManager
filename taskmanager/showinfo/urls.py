from django.urls import path
from .views import StageView, DisciplineView, \
    ApproachView, FormOfControlView, \
    AcademicWorkView, AcadmicWorkDetailView, AcademicWorkForTeacherView

urlpatterns = [
    path('stages/', StageView.as_view(), name='stage`s list'),
    path('disc/', DisciplineView.as_view(), name='disciplines list'),
    path('approaches/', ApproachView.as_view(), name='approaches list'),
    path('control/', FormOfControlView.as_view(), name='forms of control list'),
    path('academs/', AcademicWorkView.as_view(), name='academic work list'),
    path('academs/<int:pk>', AcadmicWorkDetailView.as_view(), name='academic work detail'),
    path('academs-<int:pk>', AcademicWorkForTeacherView.as_view(), name='academic work for teacher')
]