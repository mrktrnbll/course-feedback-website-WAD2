from django.urls import path
from course_feedback import views

app_name = 'course_feedback'


urlpatterns = [
    path('', views.index, name='index'),
#    path('course/', views.course, name='course'),
    path('course/<slug:course_name_slug>/', views.show_course, name='show_course'), #course would be shown on screen
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    # path('AddCourse', views.AddCourse, name='AddCourse'), #This is where they are going to be adding a course (lecturer)
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.account, name='account'),
]
