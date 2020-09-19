from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils import timezone
# from ckeditor.fields import RichTextField


# Create your models here.

class Post(models.Model):
    title = models.CharField(max_length=255)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(blank=True, null=False)
    date = models.DateField(auto_now_add=True)
    image_url = models.CharField(max_length=500, null=True)
    tag_1 = models.CharField(max_length=20)
    tag_2 = models.CharField(max_length=20)
    tag_3 = models.CharField(max_length=20)
    hearts = models.ManyToManyField(User, related_name='blog_posts')
    link_to_post = models.CharField(max_length=255, default='Read the Full Post by')

    def hearts_number(self):
        return(self.hearts.count)

    # see title/author of post in admin

    def __str__(self):
        return self.title + ' | ' + str(self.author)

    def get_absolute_url(self):
        return reverse('blog')


class Comment(models.Model):
    post_to_comment = models.ForeignKey(Post, related_name="comments", on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    comment_body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.post_to_comment.title + ' | ' + str(self.author)