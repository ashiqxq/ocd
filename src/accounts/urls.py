from django.urls import path, re_path
from accounts import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.handleLogin, name="login"),
    path("register/", views.handleSignUp, name="signup"),
    # path("faker/", views.handle_fake, name="faker1"),
    # path("scfaker/", views.student_course_fake, name="scfaker1"),
    path("logout/", views.handleLogout, name="logout")
    # re_path(r'^run/$', views.runCode, name='run')
]
