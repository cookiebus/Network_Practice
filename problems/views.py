from django.shortcuts import render, HttpResponseRedirect
from problems.forms import ProblemForm
from problems.models import Problem
from tags.models import Tag

# Create your views here.
def create(request):
    tags = Tag.objects.all()
    if request.method != "POST":
        problem_form = ProblemForm()
        return render(request, "problems/post_problem.html", locals())

    problem_form = ProblemForm(request.POST)
    if problem_form.is_valid():
        problem = problem_form.save(commit=False)
        tags = request.POST.get('tags', [])
        for tag in tags:
            tag = Tag.objects.get(id=tag)
            problem.tags.add(tag)
        problem.user = request.user
        problem.save()
        next = request.GET.get('next', '')
        if next == '':
            next = '/'
        return HttpResponseRedirect(next)

    return render(request, "problems/post_problem.html", locals())