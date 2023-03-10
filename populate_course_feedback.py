import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course-feedback-website-WAD2.settings')

import django
django.setup()
from django.contrib.auth.models import User
from course_feedback.models import Course, Review, Profile

def populate():

    reviews = {
    'CS1P':[{'content': 'I thought it was cracking', 'upvotes': 5, 'student':'simon'},
    {'content': 'Jolly good course', 'upvotes':14000, 'student':'simon'}],
    'IOOP':[{'content': 'OBJECTively brilliant', 'upvotes': 100000, 'student':'simon'},]
    }

    courses = {'CS1P': {'name': 'Computer Programming', 'reviewed': True, 'picture':'cs1p.png'},
            'IOOP': {'name': 'Introduction to Objecto Oriented Programming', 'reviewed': True, 'picture': ""}}

    students = [{'username':'simon','password':'Bigman1!','email':'simon@live.co.uk'}]

    for s in students:
        add_profile(username=s['username'],password=s['password'],email=s['email'],is_lecturer=False)

    for course, course_data in courses.items():
        c = add_course(course, course_data['name'], course_data['reviewed'],  course_data['picture'])
        for r in reviews[course]:
            add_review(c, r['content'], r['upvotes'], r['student'])

    for c in Course.objects.all():
        for r in Review.objects.filter(course=c):
            print(f'- {c}: {r}')

def add_review(course, content, upvotes, student):
    s = Profile.objects.get(user__username=student)
    r = Review.objects.get_or_create(course=course, content=content, student=s)[0]
    r.upvotes = upvotes
    r.save()
    return r

def add_course(id,name,reviewed,picture):
    c = Course.objects.get_or_create(courseID=id,name=name,reviewed=reviewed)[0]
    c.picture = picture
    c.save()
    return c

def add_profile(username, password, email, is_lecturer):
    user, created = User.objects.get_or_create(username=username, password=password, email=email)
    profile, created = Profile.objects.get_or_create(user=user, is_lecturer=is_lecturer)
    profile.save()

if __name__ == '__main__':
    print('Starting course_feedback population script')
    populate()
