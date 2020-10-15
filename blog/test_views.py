from django.contrib.auth.models import User
from django.test import Client, TestCase, RequestFactory
from . import views
from . import forms
from .models import Post, Comment


class BlogViewsTestsLoggedOut(TestCase):

    def setUp(self):
        self.client = Client()

    def test_response_200(self):
        """ test loading blog home page successful """
        response = self.client.get('/blog/')
        self.assertEqual(response.status_code, 200)

    def test_blog_loaded_templates(self):
        """ test about page loading correct templates """
        response = self.client.get('/blog/')
        templates = response.templates
        names = fetch_template_names(templates)

        self.assertIn('base.html', str(names))
        self.assertIn('blog.html', str(names))

    def test_add_post_login_required(self):
        response = self.client.get('/blog/add_post/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/admin/login/?next=/blog/add_post/"
        )

    def test_edit_post_login_required(self):
        response = self.client.get('/blog/edit_post/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/admin/login/?next=/blog/edit_post/1/"
        )

    def test_delete_post_login_required(self):
        response = self.client.get('/blog/delete_post/1/')
        self.assertEqual(response.status_code, 302)
        self.assertEqual(
            response.url,
            "/admin/login/?next=/blog/delete_post/1/"
        )

    def test_search_posts_no_query(self):
        """ test empty search query redirects user to blog """
        response = self.client.get('/blog/search/?blog_q=')
        self.assertEqual(response.url, "/blog/")
        context = response.context
        self.assertFalse(context)

    def test_search_posts_with_query(self):
        """ test search query creates context """
        response = self.client.get('/blog/search/?blog_q=test')
        context = response.context
        self.assertTrue(context)

    def test_search_posts_with_tag_query(self):
        """ test search query creates context """
        response = self.client.get('/blog/tag/test/')
        context = response.context
        self.assertTrue(context['query_term'])
        self.assertEqual(context['query_term'], 'test')


class BlogViewsTestsLoggedIn(TestCase):

    def setUp(self):
        self.factory = RequestFactory()
        self.user = User.objects.create_user(
            username='hjansen', email='hj@email.com', password='ikhebkaas42'
        )



class BlogPostViewsTestsLoggedOut(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='hjansen', email='hj@email.com', password='ikhebkaas42'
        )

    def test_response_200(self):
        post = Post.objects.create(
            title="Test Post Title",
            body="Test post body",
            author=self.user,
            tag_1='tag1',
            tag_2='tag2',
            tag_3='tag3',
        )
        """ test loading blog home page successful """
        response = self.client.get(f'/blog/blog_post/{post.id}/')
        context = response.context
        self.assertEqual(response.status_code, 200)
        self.assertEqual(context['post'], post)


class BlogPostViewsTestsNonSuperuserLoggedIn(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='hjansen', email='hj@email.com', password='ikhebkaas42'
        )

    def test_nonsuperuser_can_create_comment(self):
        """ check nonsuperuser can create comment and is
        redirected back to blog post """
        post = Post.objects.create(
            title="Test Post Title",
            author=self.user,
            body="Test post body",
            tag_1='tag1',
            tag_2='tag2',
            tag_3='tag3',
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.post(
            f'/blog/comment_post/{post.id}/',
            {
                'post_to_comment_id': post.id,
                'author': self.user.id,
                'comment_body': 'Test comment body',
            }
        )
        comment_created = Comment.objects.filter(author=self.user)
        self.assertTrue(comment_created)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/blog/blog_post/{post.id}/")

    def test_nonsuperuser_can_delete_own_comments(self):
        """ check nonsuperuser can create comment and is
        redirected back to blog post """
        post = Post.objects.create(
            title="Test Post Title",
            author=self.user,
            body="Test post body",
            tag_1='tag1',
            tag_2='tag2',
            tag_3='tag3',
        )
        comment = Comment.objects.create(
            author=self.user,
            post_to_comment=post,
            comment_body='Test comment body'
        )
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.post(
            f'/blog/delete_comment/{post.id}/',
            {
                'comment_id': comment.id
            }
        )
        comment_exists = Comment.objects.filter(author=self.user)
        self.assertFalse(comment_exists)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/blog/blog_post/{post.id}/")

    def test_nonsuperuser_can_heart_a_post(self):
        """ check nonsuperuser can create comment and is
        redirected back to blog post """
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
        client = Client()
        client.login(username='hjansen', password='ikhebkaas42')
        response = client.get(f'/blog/heart_post/{post.id}/')
        post = Post.objects.get(id=post.id)
        self.assertTrue(post.hearts)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, f"/blog/blog_post/{post.id}/")


# testing helper functions
def fetch_template_names(templates):
    template_names = []
    for t in templates:
        template_names.append(t.name)
    return template_names
