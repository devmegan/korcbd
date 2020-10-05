from django.shortcuts import render, get_object_or_404, redirect, reverse
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.admin.views.decorators import staff_member_required
from django.utils.decorators import method_decorator
from django.http import HttpResponseRedirect
from django.urls import reverse_lazy
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django.db.models import Q
from .models import Post, Comment
from .forms import AddPostForm, AddCommentForm

from collections import Counter

# Create your views here.


class Blog(ListView):
    model = Post
    template_name = 'blog/blog.html'
    ordering = ['-id']
    context = {}

    def get_context_data(self, *args, **kwargs):
        tag_list = []
        post_list = Post.objects.all()
        for post in post_list:
            tag_list.append(post.tag_1)
            tag_list.append(post.tag_2)
            tag_list.append(post.tag_3)
        counted_tags = Counter(tag_list)
        context = super(Blog, self).get_context_data(*args, **kwargs)
        context['counter'] = counted_tags.most_common(10)
        return context


def searchPosts(request):
    query_term = None
    posts = Post.objects.all()

    # handle blog searches by user
    if request.GET:
        if 'blog_q' in request.GET:
            query_term = request.GET['blog_q']
            if not query_term:
                messages.error(request, "You didn't enter any search terms")
                return redirect(reverse('blog'))

            queries = Q(title__icontains=query_term) | Q(body__icontains=query_term) | Q(tag_1__icontains=query_term) | Q(tag_2__icontains=query_term) | Q(tag_3__icontains=query_term)
            query_posts = posts.filter(queries)
        context = {
            'object_list': query_posts,
            'query_term': query_term,
        }
        return render(request, 'blog/blog.html', context)


def filterPosts(request, tag_q):
    # deslugify any slugged tags
    tag = tag_q.replace('-', ' ')
    filter_q = Q(tag_1__icontains=tag) | Q(tag_2__icontains=tag) | Q(tag_3__icontains=tag)
    # filter by tag and then pass to template as context
    tagged_posts = Post.objects.filter(filter_q)
    context = {
        'query_term': tag,
        'object_list': tagged_posts,
    }
    return render(request, 'blog/blog.html', context)


class blogPost(DetailView):
    model = Post
    template_name = 'blog/blog_post.html'

    def get_context_data(self, *args, **kwargs):
        current_post = get_object_or_404(Post, id=self.kwargs['pk'])
        hearts_number = current_post.hearts_number()
        heart_bool = False
        comment_bool = False
        if current_post.hearts.filter(id=self.request.user.id):
            heart_bool = True
        if current_post.comments.filter(id=self.request.user.id):
            comment_bool = True
        context = super(blogPost, self).get_context_data(*args, **kwargs)
        context['hearts_number'] = hearts_number
        context['heart_bool'] = heart_bool
        context['comment_bool'] = comment_bool
        context['comment_form'] = AddCommentForm()
        return context


@login_required
def commentPost(request, pk):
    # print(request.POST)
    new_comment = None
    form = AddCommentForm(request.POST)
    post_to_comment = get_object_or_404(Post, id=request.POST.get('post_to_comment_id'))
    if form.is_valid():
        new_comment = form.save(commit=False)
        new_comment.post_to_comment = post_to_comment
        new_comment.save()
    return HttpResponseRedirect(reverse('blog_post', args=[str(pk)]))


@login_required
def deleteComment(request, pk):
    comment_pk = request.POST['comment_id']
    comment_to_delete = get_object_or_404(Comment, id=comment_pk)
    comment_to_delete.delete()
    return HttpResponseRedirect(reverse('blog_post', args=[str(pk)]))


@login_required
def heartPost(request, pk):
    post_to_heart = get_object_or_404(Post, id=request.POST.get('post_id'))
    if not post_to_heart.hearts.filter(id=request.user.id).exists():
        # heart post
        post_to_heart.hearts.add(request.user)
    else:
        # unheart post
        post_to_heart.hearts.remove(request.user)
    return HttpResponseRedirect(reverse('blog_post', args=[str(pk)]))


@method_decorator(staff_member_required, name='dispatch')
class addPost(CreateView):
    model = Post
    form_class = AddPostForm
    template_name = 'blog/add_post.html'
    # fields = ('title', 'image_url', 'body', 'tag_1', 'tag_2', 'tag_3')


@method_decorator(staff_member_required, name='dispatch')
class editPost(UpdateView):
    model = Post
    form_class = AddPostForm
    template_name = 'blog/edit_post.html'
    # fields = ('title', 'image_url', 'body', 'tag_1', 'tag_2', 'tag_3')


@method_decorator(staff_member_required, name='dispatch')
class deletePost(DeleteView):
    model = Post
    template_name = 'blog/delete_post.html'
    success_url = reverse_lazy('blog')