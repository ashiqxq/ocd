from django.shortcuts import render
from accounts.models import student_assignments, student_course_bridge
from django.db.models import Subquery
from django.http import HttpResponse

status_dict = {'draft':0, 'posted':1, 'submitted':2, 'overdue':3, 'discarded':4}

# Create your views here.
def PostListViewStudent(request):
    username = request.user.username
    all_assignments = student_assignments.objects.filter(status=status_dict['posted']).filter(course_id_id__in=Subquery(student_course_bridge.objects.filter(student_id_id=username).values('course_id_id'))).select_related('course_id')
    return render(request, 'student_dashboard/s_assignment_list.html', {'assignment_list': all_assignments})

def PostDetailView(request, pk):
    assignment_det = student_assignments.objects.get(assignment_id=pk)
    return render(request, 'student_dashboard/assignment_detail_and_ide.html', {'assignment':assignment_det})