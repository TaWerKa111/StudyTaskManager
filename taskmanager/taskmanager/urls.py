from django.contrib import admin
from django.urls import path, include, re_path
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('log/', include('auth_user.urls')),
    path('teach/api/', include('showinfo.urls')),
    path('stud/api/', include('student.urls'))
]

