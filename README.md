# course-feedback-website-WAD2
Group design project for UofG WAD2 course.

28/02/2023 - Euan

In the user model I have added a is_lecturer field which has 3 options: True, False or None

I have added a file decorators.py which uses is_lecturer field with functions
to make it easier to verify the type of user

Example implementation

from django.shortcuts import render
from django.http import HttpResponse
from course_feedback import if_lecturer, if_student, if_neither

@if_lecturer
def my_view(request):
    # Your view code here
    return HttpResponse('This is a lecturer view')

-----------------------------------------------

Successfully migrated the database

Created a superuser for the database
User - euanm  Pass - 12345

-----------------------------------------------

Created the population script and successfully ran it,
although for the time being I took out the student field
in the review database as it makes the population script a cheeky
bit complicated

I need to update the population script to add a couple users but
that is a task for another day xo
