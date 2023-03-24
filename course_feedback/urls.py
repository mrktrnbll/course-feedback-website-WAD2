from django.urls import path
from course_feedback import views

app_name = 'course_feedback'

urlpatterns = [
    path('', views.index, name='index'),
    path('course/<slug:course_name_slug>/', views.show_course, name='show_course'),
    path('login/', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('logout/', views.user_logout, name='logout'),
    path('account/', views.account, name='account'),
    path('like_review/', views.LikeCourseView.as_view(), name='like_course'),
]
