from django.urls import path
from course_feedback import views

app_name = 'course_feedback'


urlpatterns = [
    path('', views.index, name='index'),
    path('course/', views.course, name='course'),
    path('login/', views.login, name='login'),
    path('register/', views.register, name='register'),
]
