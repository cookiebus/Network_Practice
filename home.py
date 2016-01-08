from django.shortcuts import render
from problems.models import Problem
from tags.models import Tag

def index(request):
    problems = Problem.objects.all()[:4]
    tags = Tag.objects.all()
    print tags
    return render(request, "index.html", locals())
