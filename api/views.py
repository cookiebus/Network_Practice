from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from problems.models import Problem
from comments.models import Comment
import json


def JsonResponse(params):
    return HttpResponse(json.dumps(params))

def signin(request):
    next = request.GET.get('next', '')

    if request.method != 'POST':
        return JsonResponse({"success": False, "error": "Please send a post."})

    if 'username_or_email'  not in request.GET:
        return JsonResponse({"success": False, "error": "Please fill username or email."})
    else:
        username_or_email = request.GET.get('username_or_email')

    if 'password'  not in request.GET:
        return JsonResponse({"success": False, "error": "Please fill password."})
    else:
        password = request.GET.get('password')

    key = 'email__iexact' if '@' in username_or_email else 'username__iexact'
    if User.objects.filter(**{key: username_or_email}).exists():
        user = User.objects.get(**{key: username_or_email})
        user = authenticate(username=user.username, password=password)
        if user is None:
            return JsonResponse({"success": False, "error": "User do not exists."})
    else:
        return JsonResponse({"success": False, "error": "User do not exists."})

    django_login(request, user)
    if 'remember' not in request.POST:
        request.session.set_expiry(0)
    else:
        request.session.set_expiry(60 * 60 * 24 * 60)

    return JsonResponse({"success": True, "id": user.id})

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
