from django.shortcuts import render, redirect
from django.http import HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from accounts.models import (
    all_users,
    teacher_user,
    student_user,
    course_list,
    student_course_bridge,
)
from faker import Faker
import random

# Create your views here.
def index(request):
    if request.user.is_authenticated:
        un = request.user.username
        us = all_users.objects.filter(username=un).values("user_type")
        if us:
            return redirect("teacher_dashboard")
        else:
            return redirect("student_dashboard")
    return render(request, "accounts/index.html")


def handleSignUp(request):
    authType = request.GET.get("type")
    if request.method == "POST":
        username = request.POST["username"]
        firstname = request.POST["firstname"]
        lastname = request.POST["lastname"]
        email = request.POST["email"]
        pass1 = request.POST["pass1"]
        pass2 = request.POST["pass2"]
        print(pass1)
        myUser = User.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=pass1,
        )
        myUser.save()
        if authType == "teacher":
            allUser = all_users(username=username, user_type=True)
            allUser.save()
            teacheruser = teacher_user(
                username=username, first_name=firstname, last_name=lastname, email=email
            )
            teacheruser.save()
            login(request, myUser)
            return redirect("teacher_dashboard")
        elif authType == "student":
            allUser = all_users(username=username, user_type=False)
            allUser.save()
            studentuser = student_user(
                username=username, first_name=firstname, last_name=lastname, email=email
            )
            studentuser.save()
            login(request, myUser)
            return redirect("student_dashboard")
        # myUser.auth_type = authType
        messages.success(request, "Your account has been successfully created")
        return redirect("home")
    else:
        return render(request, "accounts/auth/register.html", {"authType": authType})


def student_course_fake(request):
    users_list = User.objects.all()
    print(type(users_list), type(users_list[0]))
    student_user = list(all_users.objects.filter(user_type=0).values("username"))
    student_list = [dc1["username"] for dc1 in student_user]
    cl1 = list(course_list.objects.exclude(teacher_id__isnull=True))
    cl = [c.course_id for c in cl1]
    dc = {}
    for i in range(150):
        si = random.randrange(0, len(student_list))
        ci = random.randrange(0, len(cl1) - 1)
        key = "{} {}".format(si, ci)
        print(student_list[si], cl[ci])
        if key not in dc:
            dc[key] = 1
            scbridge = student_course_bridge(
                student_id_id=student_list[si], course_id_id=int(cl[ci])
            )
            scbridge.save()
    return HttpResponse("Insertion done")


def handle_fake(request):
    fake1 = Faker()
    for i in range(50):
        profile = fake1.simple_profile()
        authType = "student"
        username = profile["username"]
        name = list(profile["name"].split())
        firstname = name[0]
        lastname = name[-1]
        email = profile["mail"]
        pass1 = profile["username"]
        myUser = User.objects.create_user(
            username=username,
            first_name=firstname,
            last_name=lastname,
            email=email,
            password=pass1,
        )
        myUser.save()
        if authType == "teacher":
            allUser = all_users(username=username, user_type=True)
            allUser.save()
            teacheruser = teacher_user(
                username=username, first_name=firstname, last_name=lastname, email=email
            )
            teacheruser.save()
        elif authType == "student":
            allUser = all_users(username=username, user_type=False)
            allUser.save()
            studentuser = student_user(
                username=username, first_name=firstname, last_name=lastname, email=email
            )
            studentuser.save()
    return HttpResponse("Insertion done")


def handleLogin(request):
    authType = request.GET.get("type")
    if request.method == "POST":
        name = request.POST["name"]
        password = request.POST["pass"]
        user = authenticate(username=name, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Successfully logged in")
            if authType == "teacher":
                return redirect("teacher_dashboard")
            elif authType == "student":
                return redirect("student_dashboard")
        else:
            messages.error(request, "Invalid credentials")
        return redirect("home")
    else:
        return render(request, "accounts/auth/login.html", {"authType": authType})


def handleLogout(request):
    logout(request)
    messages.success(request, "Successfully logged out")
    return redirect("home")
