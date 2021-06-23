from student_dashboard import views
from compiler_app import views as viewsc
from django.urls import path, re_path

urlpatterns = [
    path('', views.PostListViewStudent, name='student_dashboard'),
    re_path(r'^post/run/$', viewsc.runCode, name='run'),
    re_path(r'^post/check/$', views.NewSubmission, name='check'),
    # path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>', views.PostDetailView, name='st_post_detail'),
    # path('post/new/', views.CreatePostView, name='post_new'),
    # path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post_edit'),
    # path('drafts/', views.DraftListView.as_view(), name='post_draft_list'),
    # path('post/<int:pk>/remove/', views.PostDeleteView.as_view(), name='post_remove'),
    # path('post/<int:pk>/publish/', views.post_publish, name='post_publish'),
    # path('post/<int:pk>/comment/', views.add_comment_to_post, name='add_comment_to_post'),
    # path('comment/<int:pk>/approve/', views.comment_approve, name='comment_approve'),
    # path('comment/<int:pk>/remove/', views.comment_remove, name='comment_remove'),
]