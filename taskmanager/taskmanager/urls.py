from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView
from rest_framework.documentation import include_docs_urls
from rest_framework.schemas import get_schema_view

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log/', include('auth_user.urls')),
    path('teach/api/', include('showinfo.urls')),
    path('stud/api/', include('student.urls')),
    path('docs/', include_docs_urls(title="My API title")),
    path('schema/', get_schema_view(
        title='Study Task Manager',
        description='Api for ...',
        version='0.1.1'
    ), name='openapi-schema'),
]
