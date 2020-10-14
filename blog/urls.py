from django.urls import path
from . import views

urlpatterns = [
    path('', views.Blog.as_view(), name='blog'),
    path('blog_post/<int:pk>/', views.blogPost.as_view(), name='blog_post'),
    path('search/', views.searchPosts, name='search'),
    path('add_post/', views.addPost.as_view(), name='add_post'),
    path('edit_post/<int:pk>/', views.editPost.as_view(), name='edit_post'),
    path(
        'delete_post/<int:pk>/',
        views.deletePost.as_view(),
        name='delete_post'),
    path('tag/<str:tag_q>/', views.filterPosts, name='tag'),
    path('heart_post/<int:pk>/', views.heartPost, name='heart_post'),
    path('comment_post/<int:pk>/', views.commentPost, name='add_comment'),
    path(
        'delete_comment/<int:pk>/',
        views.deleteComment,
        name='delete_comment'
    ),
]
