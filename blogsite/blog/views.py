from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from blog.forms import PostForm,CommentForm
from .models import CustomUser,Post,Comment,Like
from django.urls import reverse_lazy,reverse
from django.views.generic import CreateView,ListView,DetailView,UpdateView,DeleteView
from django.shortcuts import get_object_or_404,render,redirect,HttpResponseRedirect,HttpResponse
from django.contrib.auth.mixins import LoginRequiredMixin
from . import forms
from django.db.models import Q
from PIL import Image as Image
import base64

class SignUp(CreateView):
    form_class = forms.UserCreateForm
    success_url = reverse_lazy('blog:post_list')
    template_name = 'blog/signup.html'
    
    def form_valid(self, form):
        form.save()
        username = self.request.POST['username']
        password = self.request.POST['password1']
        user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password1'],)
        login(self.request, user)
        return HttpResponseRedirect(reverse('blog:post_list'))

class UserDetailView(DetailView):
    model = CustomUser

class UserListView(ListView):
    model = CustomUser
    context_object_name = 'user_list'
    def get_queryset(self):
        current_user = self.request.user
        if current_user.is_authenticated:
            blocked_users = current_user.blocked.all().values_list('id')
            blocked_by = [user.id for user in CustomUser.objects.all() if current_user in user.blocked.all()]
            return CustomUser.objects.filter(~Q(id__in=blocked_users)).filter(~Q(id__in=blocked_by)).exclude(is_staff=True).exclude(id__exact=current_user.id)
        else:
            return CustomUser.objects.all()
class PostListView(ListView):
    model = Post
    template_name = 'blog/post_list.html'
    def get_queryset(self):
        if self.request.user.is_authenticated:
            current_user = CustomUser.objects.get(username=self.request.user)
            blocked_users = current_user.blocked.all().values_list('id')
            blocked_by = [user for user in CustomUser.objects.all() if current_user in user.blocked.all()]
            return Post.objects.filter(~Q(author__in=blocked_users)).filter(~Q(author__in=blocked_by))

        else:
            return Post.objects.all()
class PostUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = PostForm
    model = Post

@login_required
def PostCreateView(request):
    post_form = PostForm()
    if request.method=='POST':
        user = CustomUser.objects.get(username=request.user.username)
        post_form = PostForm(request.POST,request.FILES)
        if post_form.is_valid():
            new_post = post_form.save(commit=False)
            new_post.author = user
            new_post.save()
            return redirect(new_post)
        else:
            post_form = PostForm()
    return render(request,
                  'blog/post_form.html',
                  {'form': PostForm()})
                


class PostDeleteView(LoginRequiredMixin,DeleteView):
    model = Post
    success_url = reverse_lazy('blog:post_list')

def PostDetailView(request,pk):
    post = get_object_or_404(Post, pk=pk)
    comments = post.post_comments
    new_comment = None
    if request.method == 'POST':
        user = CustomUser.objects.get(username=request.user.username)
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.author = user
            new_comment.save()
            return redirect(post)
    else:
        comment_form = CommentForm()
    return render(request,
                  'blog/post_detail.html',
                  {'post': post,
                   'comments': comments,
                   'new_comment': new_comment,
                   'comment_form': comment_form})





class CommentUpdateView(LoginRequiredMixin,UpdateView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_detail.html'
    form_class = CommentForm
    model = Comment

def delete_comment_view(request,pk):
    obj = get_object_or_404(Comment,pk=pk)
    post_id = obj.post.pk
    if request.method=='POST':
        obj.delete()
        return HttpResponseRedirect(reverse('blog:post_detail',kwargs={'pk':post_id}))
    return render(request,'blog/delete_comment.html')
        

def SuccessSignUp(request):
    return render(request,'blog/sign_up_success.html')


def BlockUser(request,pk):
    obj = get_object_or_404(CustomUser,pk=pk)
    user_id = obj.pk
    if request.method=='POST':
        user = CustomUser.objects.get(username=request.user)
        user.blocked.add(user_id)
    return HttpResponseRedirect(reverse('blog:user_details',kwargs={'pk':user_id}))


def UnblockUser(request,pk):
    obj = get_object_or_404(CustomUser,pk=pk)
    user_id = obj.pk
    if request.method=='POST':
        user = CustomUser.objects.get(username=request.user)
        user.blocked.remove(user_id)
    return HttpResponseRedirect(reverse('blog:user_details',kwargs={'pk':user_id}))

def like(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post_id = post.pk
    if request.method == 'GET':
        user = CustomUser.objects.get(username=request.user)
        user_id = user.pk
        user.liked_posts.add(post_id)
        post.liked_by.add(user_id)
    return HttpResponseRedirect(reverse("blog:post_detail",kwargs={'pk':post_id}))
def RemoveLike(request,pk):
    post = get_object_or_404(Post,pk=pk)
    post_id = post.pk
    if request.method == 'GET':
        user = CustomUser.objects.get(username=request.user)
        user_id = user.pk
        user.liked_posts.remove(post_id)
        post.liked_by.remove(user_id)
    return HttpResponseRedirect(reverse("blog:post_detail",kwargs={'pk':post_id}))