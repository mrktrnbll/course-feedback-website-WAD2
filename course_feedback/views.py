from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from django.utils.decorators import method_decorator
from django.views import View

from course_feedback.decorators import if_lecturer, if_student, if_neither
from course_feedback.models import Course, Review
from course_feedback.forms import RegisterForm, RegisterProfileForm, AddCourse, AddReview
from django.contrib.auth.decorators import login_required
from django.urls import reverse

def index(request):
    course_list = Course.objects.all()
    context_dict = {}
    context_dict['courses'] = course_list

    form = AddCourse()
    if request.method == 'POST':
        form = AddCourse(request.POST, request.FILES)
        if form.is_valid():
            course = form.save(commit=False)
            course.lecturer = request.user.profile
            course.save()
            form.save_m2m()
            return redirect('course_feedback:index')
        else:
            print(form.errors)

    course_to_review = Course.objects.filter(reviewed=False)
    context_dict['course_to_review'] = course_to_review
    context_dict['course_form'] = form
    return render(request, 'course_feedback/home.html', context_dict)


def show_course(request, course_name_slug):
    context_dict = {}

    try:
        course = Course.objects.get(slug=course_name_slug)
        reviews = Review.objects.filter(course=course)
        context_dict['reviews'] = reviews
        context_dict['course'] = course
    except Course.DoesNotExist:
        context_dict['reviews'] = None
        context_dict['course'] = None

    form = AddReview()
    if request.method == 'POST':
        form = AddReview(request.POST)

        if form.is_valid():
            review = form.save(commit=False)
            review.course = course
            review.student = request.user.profile
            review.save()
            course.reviewed = True
            course.save()
            return redirect('course_feedback:show_course', course.slug)
        else:
            print(form.errors)

    context_dict['form'] = form

    return render(request, 'course_feedback/course.html', context_dict)

def user_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(username=username, password=password)

        if user:
            if user.is_active:
                login(request, user)
                return redirect(reverse('course_feedback:index'))  #should it be course_feedback:home
            else:
                return HttpResponse("Your Campus Opinion account is disabled.")
        else:
            print(f"Invalid login details: {username}, {password}")
            return render(request, 'course_feedback/login.html', context={'registered': "We don't have any account details that match what you entered" })
    else:
        return render(request, 'course_feedback/login.html')

def user_logout(request):
    logout(request)
    return redirect(reverse('course_feedback:index'))

def register(request):
    registered = False
    if request.method == 'POST':
        user_form = RegisterForm(request.POST)
        profile_form = RegisterProfileForm(request.POST)
        if user_form.is_valid() and profile_form.is_valid():
            user = user_form.save()
            user.set_password(user.password)
            user.save()
            profile = profile_form.save(commit=False)
            profile.user = user
            profile.save()
            registered = True
            if profile.is_lecturer is True:
                return redirect(reverse('course_feedback:login'))
        else:
            print(user_form.errors, profile_form.errors)
    else:
        user_form = RegisterForm()
        profile_form = RegisterProfileForm()
    return render(request, 'course_feedback/register.html', context={'user_form': user_form, 'profile_form': profile_form, 'registered': registered})

@login_required
def add_course(request):
    if request.method == 'POST':
        course_form = AddCourse(request.POST, request.FILES)
        print(course_form.is_valid())
        print(request.FILES['picture'])
        if course_form.is_valid():
            course_form.save()
            print(request.FILES)
            if 'picture' in request.FILES:
                course_form.picture = request.FILES['picture']
            course_form.save()
            return redirect(reverse('course_feedback:index'))
        else:
            print(course_form.errors)
    else:
        course_form = AddCourse()
    return render(request, 'course_feedback/add_course.html', context={'course_form': course_form})


@login_required
def restricted(request):
    return render(request, 'course_feedback/restricted.html')


def account(request):
    student_or_lecturer = request.user.profile  # get the profile of the logged in user
    reviews = Review.objects.filter(student=student_or_lecturer)  # get all reviews made by the student
    context_dict = {'reviews': reviews}
    createdCourses = Course.objects.filter(lecturer=student_or_lecturer)
    context_dict['createdCourses'] = createdCourses
    return render(request, 'course_feedback/account.html', context_dict)


class LikeCourseView(View):
    print("i do get called")

    @method_decorator(login_required)
    def get(self, request):
        review_id = request.GET['review_id']
        try:
            review = Review.objects.get(content=review_id)
        except Review.DoesNotExist:
            return HttpResponse("")
        except ValueError:
            return HttpResponse("")

        review.upvotes = review.upvotes + 1
        review.save()

        return HttpResponse("")
        # return HttpResponse(review.upvotes)
