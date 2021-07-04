from django.urls import path, re_path
from accounts import views

urlpatterns = [
    path("", views.index, name="home"),
    path("login/", views.handleLogin, name="login"),
    path("register/", views.handleSignUp, name="signup"),
    path("logout/", views.handleLogout, name="logout"),
]
