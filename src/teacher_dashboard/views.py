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
from accounts.models import student_assignments, student_course_bridge, student_user, submission
from dateutil import parser
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Subquery
from django.db import connection
# Create your views here.
status_dict = {'draft':0, 'posted':1, 'submitted':2, 'overdue':3, 'discarded':4}


class AboutView(TemplateView):
    template_name = 'blog/about.html'


def PostDetailView(request, pk):
    assignment_det = student_assignments.objects.get(assignment_id=pk)
    course_id = assignment_det.course_id_id
    new_s = None
    with connection.cursor() as cursor:
        cursor.execute("SELECT stu.*, asub.submission_status as ss, asub.submission_id as si FROM (SELECT astu.first_name as fn, astu.last_name as ln, astu.username as un FROM accounts_student_user astu WHERE astu.username IN (SELECT student_id_id FROM accounts_student_course_bridge as ascb WHERE ascb.course_id_id=:c_id)) as stu LEFT OUTER JOIN (SELECT * FROM accounts_submission WHERE assignment_id_id=:a_id) asub ON stu.un=asub.student_id_id ORDER BY asub.submission_status DESC", {'c_id':course_id, 'a_id':pk})
        new_s = cursor.fetchall()
    return render(request, 'teacher_dashboard/post_detail.html', {'students_list':new_s, 'assignment':assignment_det})


def SubmissionDetailView(request, pk):
    submission_det = submission.objects.get(submission_id=pk)
    assignment_det = student_assignments.objects.get(assignment_id=submission_det.assignment_id_id)
    return render(request, 'teacher_dashboard/submission_detail_and_ide.html', {'assignment':assignment_det, 'submission':submission_det})



def PostListView(request):
    # return render(request, 'teacher_dashboard/base.html')
    username = request.user.username
    all_assignments = student_assignments.objects.filter(status=status_dict['posted']).filter(course_id_id__in=Subquery(course_list.objects.filter(teacher_id_id=username).values('course_id'))).select_related('course_id')
    return render(request, 'teacher_dashboard/t_assignment_list.html', {'assignment_list': all_assignments})


def DraftListView(request):
    username = request.user.username
    all_drafts = student_assignments.objects.filter(status=status_dict['draft']).filter(course_id_id__in=Subquery(course_list.objects.filter(teacher_id_id=username).values('course_id'))).select_related('course_id')
    return render(request, 'teacher_dashboard/t_draft_list.html', {'draft_list': all_drafts})


def CreatePostView(request):
    username = request.user.username
    all_courses = course_list.objects.filter(teacher_id=username)
    return render(request, 'teacher_dashboard/post_form.html', {'course_list':all_courses})


def handle_new_post(request):
    if request.method == "POST":
        pid = request.user.username
        course_id = request.POST["course_details"]
        assignment_detail = request.POST["assignment_form"]
        assignment_name = request.POST["assignment_name"]
        published_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        due_date = parser.parse(request.POST["datetime"])
        if 'save' in request.POST:
            new_assignment = student_assignments(course_id_id=course_id, assignment_body=assignment_detail,
                                                 due_date=due_date, published_date=published_date, assignment_name = assignment_name,
                                                 status=status_dict['draft'])
            new_assignment.save()
            return redirect('home')
        elif 'publish' in request.POST:
            new_assignment = student_assignments(course_id_id=course_id, assignment_body=assignment_detail,
                                                 due_date=due_date, published_date=published_date, assignment_name = assignment_name,
                                                 status=status_dict['posted'])
            new_assignment.save()
            return redirect('home')
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


# class DraftListView(LoginRequiredMixin, ListView):
#     login_url = '/login/'
#     redirect_field_name = 'blog/post_list.html'
#     Post = None
#     model = Post
#
#     def get_queryset(self):
#         return Post.objects.filter(published_date__isnull=True).order_by('created_date')


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
