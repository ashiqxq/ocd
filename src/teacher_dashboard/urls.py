from teacher_dashboard import views
from django.urls import path, re_path

urlpatterns = [
    path("", views.index, name="teacher_dashboard"),
    path("create_course/", views.handleCreateCourse, name="createCourse"),
    path("delete_course/", views.deleteCourses, name="deleteCourse"),
    path("edit_course/", views.editCourses, name="editCourse"),
    path("submission/<int:pk>", views.SubmissionDetailView, name="submission_detail"),
    path(
        "courses",
        views.courseView,
        name="tCourseView",
    ),
    path("courses/<str:course_id>", views.createAssignment, name="createAssignment"),
    path(
        "courses/<str:course_id>/edit/<slug:assignment_slug>",
        views.createAssignment,
        name="editAssignment",
    ),
    path(
        "courses/<str:course_id>/<slug:assignment_slug>",
        views.viewAssignment,
        name="viewAssignment",
    ),
    path("post/<int:pk>", views.PostDetailView, name="post_detail"),
    # path("post/new/", views.createAssignment, name="post_new"),
    path("drafts/", views.DraftListView, name="post_draft_list"),
    path(
        "new_assingment/<str:course_id>",
        views.handle_new_post,
        name="add_new_assignment",
    ),
    path(
        "new_assingment/<str:course_id>/handle_edit/<slug:assignment_slug>",
        views.handle_new_post,
        name="edit_assignment",
    ),
    path(
        "delete_assignment/<slug:assignment_slug>",
        views.deleteAssignment,
        name="delete_assignment",
    ),
]
