from django import forms
from rango.models import Profile, Course, Review


class RegisterForm(forms.ModelForm):
    username = forms.CharField(help_text="Username")
    email = forms.CharField(help_text="Email")
    password = forms.CharField(widget=forms.PasswordInput(), help_text="Password")

    class Meta:
        model = Profile
        fields = ('username', 'email', 'password',)