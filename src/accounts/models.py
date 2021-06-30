from django.db import models
from ckeditor.fields import RichTextField
from datetime import datetime
from django.utils.text import slugify

# Create your models here.
class all_users(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    user_type = models.BooleanField(default=False)


class teacher_user(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # username = models.ForeignKey(all_users, primary_key=True, on_delete=models.CASCADE)


class student_user(models.Model):
    username = models.CharField(max_length=100, primary_key=True)
    email = models.EmailField(max_length=200)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    # username = models.ForeignKey(all_users, primary_key=True, on_delete=models.CASCADE)


class course_list(models.Model):
    course_id = models.CharField(max_length=100, primary_key=True)
    course_name = models.CharField(max_length=200, null=True, blank=False)
    course_desc = models.CharField(max_length=500, null=True, blank=False)
    enrollment_code = models.CharField(
        max_length=6, null=False, default="000000", blank=False
    )
    teacher_id = models.ForeignKey(teacher_user, null=True, on_delete=models.SET_NULL)


class student_assignments(models.Model):
    assignment_id = models.AutoField(primary_key=True)
    course_id = models.ForeignKey(course_list, on_delete=models.CASCADE)
    assignment_name = models.TextField(blank=False, null=True)
    assignment_body = models.TextField(blank=False, null=True)
    published_date = models.DateTimeField(default=datetime.now)
    due_date = models.DateTimeField()
    status = models.IntegerField()
    slug = models.SlugField(null=True, unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.assignment_name)
        super(student_assignments, self).save(*args, **kwargs)


class student_course_bridge(models.Model):
    course_id = models.ForeignKey(course_list, on_delete=models.CASCADE)
    student_id = models.ForeignKey(student_user, on_delete=models.CASCADE)



class submission(models.Model):
    submission_id = models.AutoField(primary_key=True)
    assignment_id = models.ForeignKey(student_assignments, null = True, on_delete=models.SET_NULL)
    student_id = models.ForeignKey(student_user, null=True, on_delete=models.SET_NULL)
    submission_date = models.DateTimeField(default=datetime.now())
    submission_status = models.IntegerField()
    submission_code = models.TextField(blank=True, null=True)
    submission_lang = models.CharField(max_length=150, blank=True, null=True)
    #submission_status_dict::{'not_submitted': 0, 'submitted':1, 'redo':2}