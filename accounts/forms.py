from django import forms

class LoginForm(forms.Form):
    username = forms.CharField(label='Email', max_length=255)
    password = forms.CharField(widget=forms.PasswordInput())