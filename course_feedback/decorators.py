from django.shortcuts import redirect
from django.urls import reverse

def if_lecturer(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_lecturer  is True):
            return view_func(request, *args, **kwargs)
        else:
            return redirect(redirect(reverse('course_feedback:index')))  # Redirect to a different page if the user is a lecturer or not authenticated
    return wrapped_view

def if_student(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and (request.user.is_lecturer is False):
            return view_func(request, *args, **kwargs)
        else:
            return redirect('course_feedback:index')  # Redirect to a different page if the user is a lecturer or not authenticated
    return wrapped_view

def if_neither(view_func):
    def wrapped_view(request, *args, **kwargs):
        if request.user.is_authenticated and request.user.is_lecturer is None:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('course_feedback:index')  # Redirect to a different page if the user is a lecturer or not authenticated
    return wrapped_view
