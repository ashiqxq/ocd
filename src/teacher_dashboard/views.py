from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import(TemplateView, ListView,
DetailView, CreateView, UpdateView, DeleteView)
from accounts.models import course_list
# from blog.models import Post,Comment
# from blog.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from accounts.models import student_assignments
from django.http import HttpResponse
# Create your views here.


class AboutView(TemplateView):
    template_name = 'blog/about.html'


def PostListView(request):
    return render(request, 'teacher_dashboard/base.html')
# class PostListView(ListView):
#     Post = None
#     model = Post
#
# #  allows us to django's orms #lte means less than or equal to '-' in published_date helps in ordering by descending order
#     def get_queryset(self):
#         return Post.objects.filter(published_date__lte=timezone.now()).order_by('-published_date')


# class PostDetailView(DetailView):
#     model = Post

def CreatePostView(request):
    username = request.user.username
    all_courses = course_list.objects.filter(teacher_id=username)
    return render(request, 'teacher_dashboard/post_form.html', {'course_list':all_courses})

def new_draft(request):
    pass


def new_post(request):
    # pid = request.user.username
    # course_id = request.POST["course_details"]
    # assignment_detail = request.POST["assignment_form"]
    # print(assignment_detail)
    # print(request.POST["datetime"])
    # due_date = parse_datetime(request.POST["datetime"])
    # print(due_date)
    # new_assignment = student_assignments.dgs(course_id=course_id, assignment_body=assignment_detail, due_date=due_date, status=1)
    # new_assignment.save()
    # return redirect('home')


def handle_new_post(request):
    if request.method == "POST":
        if 'save' in request.POST:
            return new_draft(request)
        elif 'publish' in request.POST:
            print(request.method, "seemewgwhh meeeee")
            return new_post(request)
    return HttpResponse('hello')


# class CreatePostView(LoginRequiredMixin, CreateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#     form_class = PostForm
#     model = Post


# class PostUpdateView(LoginRequiredMixin, UpdateView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_detail.html'
#     form_class = PostForm
#     model = Post


# class PostDeleteView(LoginRequiredMixin, DeleteView):
#     model = Post
#     # redirects only after deleted
#     success_url = reverse_lazy('post_list')


class DraftListView(LoginRequiredMixin, ListView):
    login_url = '/login/'
    redirect_field_name = 'blog/post_list.html'
    Post = None
    model = Post

    def get_queryset(self):
        return Post.objects.filter(published_date__isnull=True).order_by('created_date')


###################################
##################################

# @login_required
# def post_publish(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     post.publish()
#     return redirect('post_detail', pk=pk)
#
#
# @login_required
# def add_comment_to_post(request, pk):
#     post = get_object_or_404(Post, pk=pk)
#     if request.method == 'POST':
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.save()
#             return redirect('post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/comment_form.html', {'form': form})
#
#
# @login_required
# def comment_approve(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     comment.approve()
#     return redirect('post_detail', pk=comment.post.pk)
#
#
# @login_required
# def comment_remove(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     post_pk = comment.post.pk
#     comment.delete()
#     return redirect('post_detail', pk=post_pk)
