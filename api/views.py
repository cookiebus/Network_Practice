from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from problems.models import Problem
from comments.models import Comment
import json


def JsonResponse(params):
    return HttpResponse(json.dumps(params))

def profile(request):
    if request.user.is_authenticated():
        return user(request, request.user.id)
    else:
        return user(request, 0)

def user(request, user_id):
    user_json = {}
    if int(user_id) == 0:
        user_json['email'] = 'Anonymous'
        user_json['username'] = 'Anonymous'
    else:
        user = User.objects.get(id=user_id)
        user_json['email'] = user.email
        user_json['username'] = user.username

    return JsonResponse(user_json)

def problems(request):
    problems = Problem.objects.all()
    problems_json = {}
    for problem in problems:
        problem_json = {}
        problem_json['title'] = problem.title
        problem_json['user'] = problem.user.username
        problem_json['problem_image'] = problem.problem_image.url
        problem_json['description'] = problem.description
        problem_json['up'] = problem.up
        problems_json[problem.id] = problem_json

    return JsonResponse(problems_json)

def problems_with_user(request):
    problems = Problem.objects.filter(user=request.user)
    problems_json = {}
    for problem in problems:
        problem_json = {}
        problem_json['title'] = problem.title
        problem_json['user'] = problem.user.username
        problem_json['problem_image'] = problem.problem_image.url
        problem_json['description'] = problem.description
        problem_json['up'] = problem.up
        problems_json[problem.id] = problem_json

    return JsonResponse(problems_json)

def problem(request, problem_id):
    problem_json = {}
    problem = Problem.objects.get(id=problem_id)
    problem_json['title'] = problem.title
    problem_json['user'] = problem.user.username
    problem_json['problem_image'] = problem.problem_image.url
    problem_json['description'] = problem.description
    problem_json['up'] = problem.up

    return JsonResponse(problem_json)

def comments_with_problem(request, problem_id):
    comments_json = {}
    comments = Comment.objects.filter(problem__id=problem_id)
    for comment in comments:
        comment_json = {}
        comment_json['user'] = comment.user.username
        comment_json['reply_user'] = comment.reply_user.username
        comment_json['problem'] = comment.problem.title
        comment_json['description'] = comment.description

        comments_json[comment.id] = comment_json
    
    return JsonResponse(comments_json)