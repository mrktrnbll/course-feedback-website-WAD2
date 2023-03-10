from django.db import models
from django.template.defaultfilters import slugify
from django.contrib.auth.models import User

class Profile(models.Model):
    # User model instance deals with id, username, password, email
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    # Django already has something called is_staff which does something we don't want
    # So I have changed name to isLecturer for clarity
    is_lecturer = models.NullBooleanField(default=None)
    # Default = None means they are neither student nor lecturer
    # If set to True, then they have lecturer permissions, if set to false they have student permissions

    def __str__(self):
        return self.user.username

    def get_is_lecturer(self):
        return self.is_lecturer

class Course(models.Model):
    NAME_MAX_LENGTH = 128
    ID_MAX_LENGTH = 8

    courseID = models.CharField(max_length=ID_MAX_LENGTH, unique=True, primary_key=True)
    name = models.CharField(max_length=NAME_MAX_LENGTH, unique=True)
    lecturer = models.ForeignKey(Profile, on_delete=models.SET_NULL, null=True)
    # No CASCADE above as if a Lecturer account is deleted the course is allowed to live
    reviewed = models.BooleanField(default=False)
    picture = models.ImageField(upload_to='course_images', null=True)
    slug = models.SlugField(unique=True)

    def save(self, *args, **kwargs):
        self.slug = slugify(self.courseID)
        super(Course, self).save(*args, **kwargs)

    def __str__(self):
        return self.courseID

class Review(models.Model):
    CONTENT_MAX_LENGTH = 500

    content = models.CharField(max_length=CONTENT_MAX_LENGTH, unique=True)  # unique means no spam
    upvotes = models.IntegerField(default = 0)
    course = models.ForeignKey(Course, on_delete=models.CASCADE)
#    student = models.ForeignKey(Profile, on_delete=models.CASCADE)
#   temporarily removing the tie to the student because it is a bit complex to implement so need more time

    def __str__(self):
        return self.content
