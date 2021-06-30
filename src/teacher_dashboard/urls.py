from teacher_dashboard import views
<<<<<<< HEAD
from compiler_app.views import runCode
from django.urls import path

urlpatterns = [
    path('', views.PostListView, name='teacher_dashboard'),
    # path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>', views.PostDetailView, name='post_detail'),
    path('submission/<int:pk>', views.SubmissionDetailView, name='submission_detail'),
    path('submission/run/', runCode, name='t_run'),
    path('post/new/', views.CreatePostView, name='post_new'),
    path('drafts/', views.DraftListView, name='post_draft_list'),
    # path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    path('new_assingment/', views.handle_new_post, name='add_new_assignment'),
    # path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    # path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    # path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    # path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]
# urlpatterns = [
#     path('',views.PostListView.as_view(),name='post_list'),
#     path('about/',views.AboutView.as_view(),name='about'),
#     path('post/<int:pk>', views.PostDetailView.as_view(), name='post_detail'),
#     path('post/new/', views.CreatePostView.as_view(), name='post_new'),
#     path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
#     path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
#     path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
#     path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
#     path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
#     path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
#     path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
# ]
=======
from django.urls import path, re_path

urlpatterns = [
    path("", views.index, name="teacher_dashboard"),
    path("create_course/", views.handleCreateCourse, name="createCourse"),
    path("delete_course/", views.deleteCourses, name="deleteCourse"),
    path("edit_course/", views.editCourses, name="editCourse"),
    path('submission/<int:pk>', views.SubmissionDetailView, name='submission_detail'),
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
>>>>>>> c5c0588df3f1c9891630d72e86d2f9b24b56745d
