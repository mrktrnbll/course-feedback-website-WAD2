from django import forms
from django.contrib.auth.models import User
from course_feedback.models import Profile, Course, Review


class RegisterForm(forms.ModelForm):
    # username = forms.CharField(help_text="Username")
    # email = forms.CharField(help_text="Email")
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)


class RegisterProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('is_lecturer',)


class LoginForm(forms.ModelForm):
    # username = forms.CharField(help_text="Username")
    # password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")

    class Meta:
        model = User
        fields = ('username', 'password',)


class AddReview(forms.ModelForm):
    content = forms.CharField(help_text="Enter feedback here.")

    class Meta:
        model = Review
        fields = ('content',)


class AddCourse(forms.ModelForm):
    courseID = forms.CharField()
    name = forms.CharField()
    picture = forms.ImageField()

    class Meta:
        model = Course
        fields = ('courseID', 'name', 'picture')
