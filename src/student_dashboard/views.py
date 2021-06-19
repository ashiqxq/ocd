from django.shortcuts import render
# Create your views here.
def PostListViewStudent(request):
    return render(request, 'student_dashboard/base.html')