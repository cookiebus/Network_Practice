# coding: utf-8
from django import forms
from problems.models import Problem


class ProblemForm(forms.ModelForm):

    class Meta:
        model = Problem
        fields = ('title', 'problem_image', 'description')