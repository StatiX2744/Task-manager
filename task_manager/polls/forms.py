from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import get_user_model

User = get_user_model()

class RegisterForm(UserCreationForm):
    first_name = forms.CharField()
    last_name = forms.CharField()
    email = forms.EmailField()

    class Meta:
        model = User
        fields = ('first_name','last_name', 'username', 'email', 'password1' ,'password2')

class LoginForm(forms.Form):
    username = forms.CharField(max_length=65)
    password = forms.CharField(max_length=65, widget=forms.PasswordInput)

class CreateTaskForm(forms.Form):
    title = forms.CharField(max_length=128)
    description = forms.CharField(max_length=512,required=False)
    private = forms.BooleanField(required=False)
    userList = forms.CharField(max_length=1024,required=False)
    teamList = forms.CharField(max_length=1024,required=False)

class DeleteTaskForm(forms.Form):
    id = forms.IntegerField()

class CreateTeamForm(forms.Form):
    name = forms.CharField(max_length=65)