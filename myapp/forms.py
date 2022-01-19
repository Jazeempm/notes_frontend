from django import forms

class LoginForm(forms.Form):
    username=forms.CharField(label='Your name', max_length=100)
    password=forms.CharField(widget=forms.PasswordInput())


class RegisterForm(LoginForm):
    email = forms.EmailField()

class NotesForm(forms.Form):
    title=forms.CharField(max_length=100)
    content=forms.CharField(max_length=1000)
    created=forms.DateTimeField(required=False)