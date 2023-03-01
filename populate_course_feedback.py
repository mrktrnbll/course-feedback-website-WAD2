import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'course-feedback-website-WAD2.settings')

import django
django.setup()
from course_feedback.models import Course, Review

def populate():

    cs1p_reviews = [{'content': 'I thought it was cracking', 'upvotes': 5},
    {'content': 'Jolly good course', 'upvotes':14000}]

    courses = {'CS1P': {'reviews': cs1p_reviews, 'name': 'Computer Programming', 'reviewed': True, 'picture':'cs1p.png'},
            'IOOP': {'reviews': [], 'name': 'Introduction to Objecto Oriented Programming', 'reviewed': False, 'picture': ""}}

    for course, course_data in courses.items():
        c = add_course(course, course_data['name'], course_data['reviewed'],  course_data['picture'])
        for r in course_data['reviews']:
            add_review(c, r['content'], r['upvotes'])

    for c in Course.objects.all():
        for r in Review.objects.filter(course=c):
            print(f'- {c}: {r}')

def add_review(course, content, upvotes):
    r = Review.objects.get_or_create(course=course, content=content)[0]
    r.upvotes = upvotes
    r.save()
    return r

def add_course(id,name,reviewed,picture):
    c = Course.objects.get_or_create(courseID=id,name=name,reviewed=reviewed)[0]
    c.picture = picture
    c.save()
    return c

if __name__ == '__main__':
    print('Starting course_feedback population script')
    populate()
