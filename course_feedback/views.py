from django.shortcuts import render

# Create your views here.


def index(request):
    return render(request, 'course_feedback/home.html')

def course(request):
    return render(request, 'course_feedback/course.html')

def login(request):
    return render(request, 'course_feedback/login.html')

def register(request):
    return render(request, 'course_feedback/register.html')