from django.http.response import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import render, redirect
from accounts.models import (
    student_assignments,
    student_course_bridge,
    course_list,
    student_user,
    submission,
)
from django.db.models import Subquery
from datetime import datetime
from django.http import HttpResponse

status_dict = {"draft": 0, "posted": 1, "submitted": 2, "overdue": 3, "discarded": 4}
submission_status_dict = {"not_submitted": 0, "submitted": 1, "redo": 2}


def index(request):
    username = request.user.username
    all_courses = course_list.objects.filter(
        course_id__in=Subquery(
            student_course_bridge.objects.filter(student_id_id=username).values(
                "course_id_id"
            )
        )
    )
    return render(request, "student_dashboard/home.html", {"courses": all_courses})


def enrollCourse(request):
    username = request.user.username
    if request.method == "POST":
        enroll_code = request.POST["enroll_code"]
        course = course_list.objects.get(enrollment_code=enroll_code)
        student = student_user.objects.get(username=username)
        bridge = student_course_bridge(course_id=course, student_id=student)
        bridge.save()
    return redirect("shome")


def courseView(request):
    courseID = request.GET.get("course_id")
    course = course_list.objects.get(course_id=courseID)
    username = request.user.username
    all_assignments = student_assignments.objects.filter(
        status=status_dict["posted"]
    ).filter(course_id=courseID)
    return render(
        request,
        "student_dashboard/course_view.html",
        {"course": course, "assignment_list": all_assignments},
    )


def viewAssignment(request, course_id, assignment_slug):
    course = course_list.objects.get(course_id=course_id)
    assignment = student_assignments.objects.get(slug=assignment_slug)
    username = request.user.username
    submissions = submission.objects.filter(
        assignment_id_id=assignment.assignment_id, student_id_id=username
    )
    print(username)
    print(submissions)
    return render(
        request,
        "student_dashboard/assignment_detail_and_ide.html",
        {"course": course, "assignment": assignment},
    )


def NewSubmission(request):
    if request.is_ajax():
        source = request.POST["source"]
        lang = request.POST["lang"]
        assignment_id = int(request.POST["pk"])
        username = request.user.username
        submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_submitted = 0
        try:
            is_sub = submission.objects.get(
                student_id_id=username, assignment_id=assignment_id
            )
            is_submitted = 1
        except:
            pass
        if not is_submitted:
            new_submission = submission(
                assignment_id_id=assignment_id,
                submission_date=submission_date,
                student_id_id=username,
                submission_lang=lang,
                submission_status=submission_status_dict["submitted"],
                submission_code=source,
            )
            new_submission.save()
        print("successfully submitted")
        res = {
            "run_status": {
                "memory_used": "2744",
                "time_limit": 5,
                "output_html": "Hello&nbsp;world<br>",
                "memory_limit": 262144,
                "time_used": "1.402842",
                "signal": "OTHER",
                "exit_code": "0",
                "status_detail": "NA",
                "status": "AC",
                "stderr": "",
                "output": "Hello world\n",
                "async": 0,
                "request_NOT_OK_reason": "",
                "request_OK": "True",
            },
            "compile_status": "OK",
            "code_id": "42bb58K",
            "submission_status": is_submitted,
        }
        return JsonResponse(res, safe=False)

    else:
        return HttpResponseForbidden()


# Create your views here.
def PostListViewStudent(request):
    username = request.user.username
    all_assignments = (
        student_assignments.objects.filter(status=status_dict["posted"])
        .filter(
            course_id_id__in=Subquery(
                student_course_bridge.objects.filter(student_id_id=username).values(
                    "course_id_id"
                )
            )
        )
        .select_related("course_id")
    )
    return render(
        request,
        "student_dashboard/s_assignment_list.html",
        {"assignment_list": all_assignments},
    )


def PostDetailView(request, pk):
    assignment_det = student_assignments.objects.get(assignment_id=pk)
    return render(
        request,
        "student_dashboard/assignment_detail_and_ide.html",
        {"assignment": assignment_det},
    )
