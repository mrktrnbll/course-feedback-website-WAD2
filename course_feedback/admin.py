from django.contrib import admin
from course_feedback.models import Profile, Course, Review

class CourseAdmin(admin.ModelAdmin):
    list_display = ('courseID','name','lecturer','reviewed')

class ReviewAdmin(admin.ModelAdmin):
    list_display = ('content', 'upvotes', 'course')

admin.site.register(Course, CourseAdmin)
admin.site.register(Review, ReviewAdmin)
admin.site.register(Profile)
