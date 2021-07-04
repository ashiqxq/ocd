"""src URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import re_path, path, include

# from compiler_app import views

urlpatterns = [
    path("", include("accounts.urls"), name="home"),
    path("ide/", include("compiler_app.urls"), name="compiler"),
    path("accounts/", include("accounts.urls"), name="accounts"),
    path("admin/", admin.site.urls, name="admin"),
    path(
        "teacher_dashboard/",
        include("teacher_dashboard.urls"),
        name="teacher_dashboard",
    ),
    path(
        "student_dashboard/",
        include("student_dashboard.urls"),
        name="student_dashboard",
    ),
    # re_path(r"^run/$", views.runCode, name="run"),
]
