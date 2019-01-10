from django.shortcuts import render , get_object_or_404 , redirect
from django.utils import timezone
from django.http import HttpResponse
from blog.models import Post , Comment
from blog.forms import PostForm , CommentForm
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import (TemplateView , ListView , UpdateView, DetailView , CreateView, DeleteView)
# Create your views here.

class AboutView(TemplateView):
    fields = '__all__'
    template_name = 'about.html'

class PostListView(ListView):
    fields = '__all__'
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__lte = timezone.now()).order_by('-published_date')

class PostDetailView(DetailView):
    fields = '__all__'
    model = Post

class CreatePostView(LoginRequiredMixin , CreateView):
    fields = '__all__'
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    from_class = PostForm
    model = Post

class PostUpdateView(LoginRequiredMixin , CreateView):
    fields = '__all__'
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    from_class = PostForm
    model = Post

class PostDeleteView(LoginRequiredMixin , DeleteView):
    fields = '__all__'
    model = Post
    success_url = reverse_lazy('post_list')

@login_required
def post_publish(request , pk):
    post = get_object_or_404(Post , pk = pk)
    post.publish()
    return redirect('post_detail' , pk = pk)

@login_required
def add_comment_to_post(request , pk):
    post = get_object_or_404(Post , pk = pk)
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit = False)
            comment.post = post
            comment.save()
            return redirect('post_detail' ,pk = post.pk)
    else:
        form = CommentForm()
    return render(request , 'blog/comment_form.html' , {'form':form})

@login_required
def comment_approve(request , pk):
    comment = get_object_or_404(Comment , pk = pk)
    comment.approve()
    comment.save()
    return redirect('post_detail' , pk = comment.post.pk)

@login_required
def comment_remove(request , pk):
    comment = get_object_or_404(Comment , pk = pk)
    post_pk = comment.post.pk
    comment.delete()
    return redirect('post_detail' , pk = post_pk)
