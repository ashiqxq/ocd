from django.http.response import HttpResponseForbidden
from django.http import JsonResponse
from django.shortcuts import render
from accounts.models import student_assignments, student_course_bridge, submission
from django.db.models import Subquery
from datetime import datetime
from django.http import HttpResponse

status_dict = {'draft':0, 'posted':1, 'submitted':2, 'overdue':3, 'discarded':4}
submission_status_dict = {'not_submitted': 0, 'submitted':1, 'redo':2}

# Create your views here.
def check(request):
    return PostListViewStudent(request)


def NewSubmission(request):
    if request.is_ajax():
        source = request.POST['source']
        lang = request.POST['lang']
        assignment_id = int(request.POST['pk'])
        username = request.user.username
        submission_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        is_submitted = 0
        try:
            is_sub = submission.objects.get(student_id_id=username, assignment_id=assignment_id)
            is_submitted = 1
        except:
            pass
        if not is_submitted:
            new_submission = submission(assignment_id_id=assignment_id,
                                                 submission_date=submission_date,
                                                 student_id_id=username, submission_lang=lang,
                                                 submission_status=submission_status_dict['submitted'], submission_code=source)
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
                "request_OK": "True"
            },
            "compile_status": "OK",
            "code_id": "42bb58K",
            "submission_status": is_submitted
        }
        return JsonResponse(res, safe=False)

    else:
        return HttpResponseForbidden()


def PostListViewStudent(request):
    username = request.user.username
    all_assignments = student_assignments.objects.filter(status=status_dict['posted']).filter(course_id_id__in=Subquery(student_course_bridge.objects.filter(student_id_id=username).values('course_id_id'))).select_related('course_id')
    return render(request, 'student_dashboard/s_assignment_list.html', {'assignment_list': all_assignments})

def PostDetailView(request, pk):
    assignment_det = student_assignments.objects.get(assignment_id=pk)
    return render(request, 'student_dashboard/assignment_detail_and_ide.html', {'assignment':assignment_det})