from django.urls import path
from .views import Blog, searchPosts, blogPost, addPost, editPost, deletePost, filterPosts, heartPost, commentPost, deleteComment

urlpatterns = [
    path('', Blog.as_view(), name='blog'),
    path('blog_post/<int:pk>', blogPost.as_view(), name='blog_post'),
    path('search/', searchPosts, name='search'),
    path('add_post/', addPost.as_view(), name='add_post'),
    path('edit_post/<int:pk>', editPost.as_view(), name='edit_post'),
    path('delete_post/<int:pk>', deletePost.as_view(), name='delete_post'),
    path('tag/<str:tag_q>', filterPosts, name='tag'),
    path('heart_post/<int:pk>', heartPost, name='heart_post'),
    path('comment_post/<int:pk>', commentPost, name='add_comment'),
    path('delete_comment/<int:pk>', deleteComment, name='delete_comment'),
]