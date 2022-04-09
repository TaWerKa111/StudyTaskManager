from django.urls import path
from .views import AcademicWorksView

urlpatterns = [
    path('academs/<int:pk>', AcademicWorksView.as_view(), name='student`s works'),
]
