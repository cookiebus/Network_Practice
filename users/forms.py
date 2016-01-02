# coding: utf-8
from django import forms
from django.contrib.auth.models import User


class SignupForm(forms.ModelForm):

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class SigninForm(forms.Form):
    username_or_email = forms.CharField(label=u"账号", max_length=255)
    password = forms.CharField(label=u"密码", max_length=100, widget = forms.PasswordInput)