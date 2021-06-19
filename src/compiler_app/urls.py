from django.urls import path, re_path
from compiler_app import views

urlpatterns = [
        path('', views.index, name='ide'),
        re_path(r'^run/$', views.runCode, name='run')
    ]