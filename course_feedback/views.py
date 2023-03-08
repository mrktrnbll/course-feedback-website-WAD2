from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse
from course_feedback.decorators import if_lecturer, if_student, if_neither
from course_feedback.models import Course 
from course_feedback.forms import RegisterForm, RegisterProfileForm
from django.contrib.auth.decorators import login_required
from course_feedback.forms import AddCourse
from django.urls import reverse
# Create your views here.


# def if_lecturer(user):
#     return user.groups.filter(name='lecturer').exists()


# @login_required
# @if_lecturer
def index(request):
    course_list = Course.objects.all()
    context_dict = {}
    context_dict['courses'] = course_list
    #visitor_cookie_handler(request) - if we want to see the amount of people who will be visiting the site


    return render(request, 'course_feedback/home.html', context=context_dict)

# def course(request):

#     return render(request, 'course_feedback/course.html')

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
            return HttpResponse("Invalid login details supplied.")
    else:
        return render(request, 'course_feedback/login.html')

# @login_required
def user_logout(request):
    logout(request)
    return redirect(reverse('course_feedback:index'))



# @login_required
# @if_lecturer
def my_view(request):
    return HttpResponse('This is the lecturer view')



# def if_student(user):
#     return user.groups.filter(name='student').exists()


# @if_student
def my_view(request):

    return HttpResponse('This is the student view')


# @if_neither
def my_view(request):
    return render(request, 'course_feedback/home.html')
    

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
def course(request):
    if request.method == 'POST':
        form = AddCourse(request.POST)
        print("here")
        if form.is_valid():
            form = form.save()
            print(request.FILES)
            if 'picture' in request.FILES:
                print("its here")
                form.picture = request.FILES['picture']
            elif 'photo' in request.method:
                print('its in photo')
            form.save()
            return redirect(reverse('course_feedback:index')) #should it be course_feedback:home
        else:
            print(form.errors)
    else:
        form = AddCourse()
        print("INNN HEEREEE ")
    return render(request, 'course_feedback/course.html', context={'form': form})


@login_required
def restricted(request):
    return render(request, 'course_feedback/restricted.html')


def account(request):
    return render(request, 'course_feedback/account.html')


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