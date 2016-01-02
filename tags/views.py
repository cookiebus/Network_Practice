from django.shortcuts import render, HttpResponseRedirect, get_object_or_404
from ratelimit.decorators import ratelimit
from tags.models import Tag
# Create your views here.

def tags(request, id):
    tag = get_object_or_404(Tag, pk=id)
    problems = tag.problem_set.all()
    return render(request, "index.html", locals())
