from django import forms
from django.contrib.auth.models import User
from course_feedback.models import Profile, Course, Review


class RegisterForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput(attrs={'class':'register_boxes',}))

    class Meta:
        model = User
        fields = ('username', 'email', 'password',)
        help_texts = {
            'username': None,
            'password': None,
        }

        widgets = {
            'username': forms.TextInput(attrs={'class': 'register_boxes'}),
            'email': forms.TextInput(attrs={'class': 'register_boxes'}),
        }


class RegisterProfileForm(forms.ModelForm):

    class Meta:
        model = Profile
        fields = ('is_lecturer',)
        help_texts = {
            'username': None,
            'password': None,
        }

        widgets = {
        }


class LoginForm(forms.ModelForm):
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
