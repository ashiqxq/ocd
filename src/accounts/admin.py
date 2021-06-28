from django.contrib import admin
from accounts.models import (
    all_users,
    teacher_user,
    student_user,
    course_list,
    student_course_bridge,
)

# Register your models here.

admin.site.register(all_users)
admin.site.register(teacher_user)
admin.site.register(student_user)
admin.site.register(course_list)
admin.site.register(student_course_bridge)
