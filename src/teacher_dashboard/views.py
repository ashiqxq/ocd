from django.shortcuts import render, get_object_or_404, redirect
from django.utils.crypto import get_random_string
from django.views.generic import (
    TemplateView,
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
)

# from blog.models import Post,Comment
# from blog.forms import PostForm, CommentForm
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from django.utils.dateparse import parse_datetime
from accounts.models import student_assignments, teacher_user, course_list, submission
from dateutil import parser
from dateutil import tz
from django.http import HttpResponse
from datetime import datetime
from django.db.models import Subquery
from django.contrib.auth.decorators import login_required

# Create your views here.
status_dict = {"draft": 0, "posted": 1, "submitted": 2, "overdue": 3, "discarded": 4}


IST = tz.gettz("Asia/Kolkata")
tzinfos = {"IST": IST}


class AboutView(TemplateView):
    template_name = "blog/about.html"


def PostDetailView(request, pk):
    pass


@login_required(login_url="/accounts/login?type=student")
def index(request):
    username = request.user.username
    courses = getCourses(username)
    return render(request, "teacher_dashboard/home.html", {"courses": courses})


@login_required(login_url="/accounts/login?type=student")
def handleCreateCourse(request):
    username = request.user.username
    teacher = teacher_user.objects.get(username=username)
    if request.method == "POST":
        courseID = request.POST["courseID"]
        courseTitle = request.POST["courseTitle"]
        courseDesc = request.POST["courseDesc"]
        enrollment_code = get_random_string(6)
        course = course_list(
            course_id=courseID,
            course_name=courseTitle,
            course_desc=courseDesc,
            enrollment_code=enrollment_code,
            teacher_id=teacher,
        )
        course.save()
    return redirect("teacher_dashboard")


def getCourses(teacherID):
    all_courses = course_list.objects.all().filter(teacher_id_id=teacherID)
    return all_courses


@login_required(login_url="/accounts/login?type=student")
def deleteCourses(request):
    courseID = request.GET.get("course_id")
    course = course_list.objects.get(course_id=courseID)
    course.delete()
    return redirect("teacher_dashboard")


@login_required(login_url="/accounts/login?type=student")
def editCourses(request):
    courseID = request.GET.get("course_id")
    if request.method == "POST":
        courseID = request.POST["courseID"]
        course = course_list.objects.get(course_id=courseID)
        courseTitle = request.POST["courseTitle"]
        courseDesc = request.POST["courseDesc"]
        course.course_name = courseTitle
        course.course_desc = courseDesc
        course.save()
    return redirect("teacher_dashboard")


@login_required(login_url="/accounts/login?type=student")
def courseView(request):
    courseID = request.GET.get("course_id")
    course = course_list.objects.get(course_id=courseID)
    username = request.user.username
    all_assignments = student_assignments.objects.filter(
        status=status_dict["posted"]
    ).filter(course_id=courseID)
    # print(all_assignments)
    return render(
        request,
        "teacher_dashboard/course_view.html",
        {"course": course, "assignment_list": all_assignments},
    )


# def getTeacherName(teacherName):
#     teacher = teacher_user.objects.get(username=teacherName)
#     return teacher.first_name + " " + teacher.last_name


@login_required(login_url="/accounts/login?type=student")
def PostListView(request):
    # return render(request, 'teacher_dashboard/base.html')
    username = request.user.username
    all_assignments = (
        student_assignments.objects.filter(status=status_dict["posted"])
        .filter(
            course_id_id__in=Subquery(
                course_list.objects.filter(teacher_id_id=username).values("course_id")
            )
        )
        .select_related("course_id")
    )
    return render(
        request,
        "teacher_dashboard/t_assignment_list.html",
        {"assignment_list": all_assignments},
    )


@login_required(login_url="/accounts/login?type=student")
def DraftListView(request):
    username = request.user.username
    all_drafts = (
        student_assignments.objects.filter(status=status_dict["draft"])
        .filter(
            course_id_id__in=Subquery(
                course_list.objects.filter(teacher_id_id=username).values("course_id")
            )
        )
        .select_related("course_id")
    )
    return render(
        request, "teacher_dashboard/t_draft_list.html", {"draft_list": all_drafts}
    )


@login_required(login_url="/accounts/login?type=student")
def createAssignment(request, course_id, assignment_slug=None):
    username = request.user.username
    course = course_list.objects.get(course_id=course_id)
    if assignment_slug:
        assignment = student_assignments.objects.get(slug=assignment_slug)
        return render(
            request,
            "teacher_dashboard/post_form.html",
            {"course": course, "assignment": assignment},
        )
    else:
        return render(request, "teacher_dashboard/post_form.html", {"course": course})


@login_required(login_url="/accounts/login?type=student")
def handle_new_post(request, course_id, assignment_slug=None):
    if request.method == "POST":
        pid = request.user.username
        assignment_detail = request.POST["assignment_form"]
        assignment_name = request.POST["assignment_name"]
        published_date = datetime.now(tz=IST).strftime("%Y-%m-%d %H:%M:%S")
        due_date = request.POST["date"].split(" ")[0]
        due_time = request.POST["time"]
        assignment_due = parser.parse(f"{due_date} {due_time}:00", tzinfos=tzinfos)
        if "save" in request.POST:
            new_assignment = student_assignments(
                course_id_id=course_id,
                assignment_body=assignment_detail,
                due_date=assignment_due,
                published_date=published_date,
                assignment_name=assignment_name,
                status=status_dict["draft"],
            )
            new_assignment.save()
            return redirect("teacher_dashboard")
        elif "publish" in request.POST:
            new_assignment = student_assignments(
                course_id_id=course_id,
                assignment_body=assignment_detail,
                due_date=assignment_due,
                published_date=published_date,
                assignment_name=assignment_name,
                status=status_dict["posted"],
            )
            new_assignment.save()
            return redirect("teacher_dashboard")
        elif "edit" in request.POST:
            assignment = student_assignments.objects.get(slug=assignment_slug)
            assignment.assignment_name = assignment_name
            assignment.assignment_body = assignment_detail
            assignment.due_date = assignment_due
            assignment.save()
            return redirect("teacher_dashboard")
    return HttpResponse("hello")


@login_required(login_url="/accounts/login?type=student")
def viewAssignment(request, course_id, assignment_slug):
    course = course_list.objects.get(course_id=course_id)
    assignment = student_assignments.objects.get(slug=assignment_slug)
    all_submission_det = submission.objects.filter(
        assignment_id=assignment.assignment_id
    )
    return render(
        request,
        "teacher_dashboard/assignment_view.html",
        {"course": course, "assignment": assignment, "submissions": all_submission_det},
    )


@login_required(login_url="/accounts/login?type=student")
def deleteAssignment(request, assignment_slug):
    assignment = student_assignments.objects.get(slug=assignment_slug)
    assignment.delete()
    return redirect("home")


@login_required(login_url="/accounts/login?type=student")
def SubmissionDetailView(request, pk):
    submission_det = submission.objects.get(submission_id=pk)
    assignment_det = student_assignments.objects.get(
        assignment_id=submission_det.assignment_id_id
    )
    return render(
        request,
        "teacher_dashboard/submission_detail_and_ide.html",
        {"assignment": assignment_det, "submission": submission_det},
    )
