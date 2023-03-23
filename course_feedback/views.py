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

# @login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('course_feedback:index'))


# def if_student(user):
#     return user.groups.filter(name='student').exists()


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
                print("lecture is chosen, mention that an admin will need to authenticate at a later date.")
                ## we will want to add some sort of returning message here to show the user that they
                ## a lecturer yet
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
        print("here")
        review_id = request.GET['content']
        print("i even get here " + review_id)
        try:
            review = Review.objects.get(content=review_id)
        except Review.DoesNotExist:
            return HttpResponse(-1)
        except ValueError:
            return HttpResponse(-1)

        review.upvotes = review.upvotes + 1
        review.save()

        return HttpResponse(review.upvotes)


# def visitor_cookie_handler(request):
#     visits = int(get_server_side_cookie(request, 'visits', '1'))
#     last_visit_cookie = get_server_side_cookie(request, 'last_visit', str(datetime.now()))
#     last_visit_time = datetime.strptime(last_visit_cookie[:-7], '%Y-%m-%d %H:%M:%S')

#     if (datetime.now() - last_visit_time).days > 0:
#         visits = visits + 1
#         request.session['last_visit'] = str(datetime.now())
#     else:
#         request.session['last_visit'] = last_visit_cookie

#     request.session['visits'] = visits
