from teacher_dashboard import views
from django.urls import path

urlpatterns = [
    path('', views.PostListView, name='teacher_dashboard'),
    # path('about/', views.AboutView.as_view(), name='about'),
    path('post/<int:pk>', views.PostDetailView, name='post_detail'),
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
