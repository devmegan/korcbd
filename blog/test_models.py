from django.contrib.auth.models import User
from django.test import TestCase, RequestFactory, Client
from .models import Post, Comment


class AboutModelTests(TestCase):

    def setUp(self):
        # create a test user
        self.factory = RequestFactory()
        self.user = User.objects.create_superuser(
            username='hjansen',
            email='hj@email.com',
            password='ikhebkaas42',
        )

    def test_post_string_representation(self):
        """ test string representation of blog posts """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        post = Post.objects.create(
            title="Test Post Title",
            author=self.user,
            body="Test post body",
            tag_1='tag1',
            tag_2='tag2',
            tag_3='tag3',
        )
        self.assertEqual(str(post), f'{post.title} | {post.author}')

    def test_comment_string_representation(self):
        """ test string representation of blog comments """
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        post = Post.objects.create(
            title="Test Post Title",
            author=self.user,
            body="Test post body",
            tag_1='tag1',
            tag_2='tag2',
            tag_3='tag3',
        )
        comment = Comment.objects.create(
            post_to_comment=post,
            author=self.user,
            comment_body="Test comment body",
        )
        self.assertEqual(
            str(comment),
            f'{comment.post_to_comment.title} | {comment.author}'
        )
