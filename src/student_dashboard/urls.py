from student_dashboard import views
from compiler_app import views as viewsc
from django.urls import path, re_path

urlpatterns = [
    path("", views.index, name="student_dashboard"),
    # path("", views.index, name="home"),
    path("enrollCourse/", views.enrollCourse, name="enrollCourse"),
    re_path(
        r"^courses(?:course_id=(?P<course_id>\d+)/)?$",
        views.courseView,
        name="scourseView",
    ),
    path(
        "courses/<str:course_id>/<slug:assignment_slug>",
        views.viewAssignment,
        name="sviewAssignment",
    ),
    re_path(r"^run/$", viewsc.runCode, name="run"),
    re_path(r"^submit/$", views.NewSubmission, name="submit"),
    path("post/<int:pk>", views.PostDetailView, name="st_post_detail"),
]
