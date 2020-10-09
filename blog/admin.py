from django.contrib import admin
from .models import Post, Comment

# Register your models here.

# Access blog posts in admin area
admin.site.register(Post)
admin.site.register(Comment)
