from django.shortcuts import render, HttpResponse, HttpResponseRedirect
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, authenticate
from problems.models import Problem
from comments.models import Comment
from tags.models import Tag
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json, os, random

@csrf_exempt
def JsonResponse(params):
    return HttpResponse(json.dumps(params))

@csrf_exempt
def post_tag(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Please send a post."})
    
    if 'tag_name' not in request.POST or len(request.POST.get('tag_name'))==0:
        return JsonResponse({"success": False, "error": "Please fill tag name."})
    else:
        tag_name = request.POST.get('tag_name')

    tag = Tag.objects.create(name=tag_name)
    return JsonResponse({"success": True, "id": tag.id})
    
@csrf_exempt
def post_problem(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Please send a post."})

    if 'user_id' not in request.POST or len(request.POST.get('user_id'))==0:
        return JsonResponse({"success": False, "error": "Please login first"})
    else:
        user_id = request.POST.get('user_id')

    if 'title' not in request.POST or len(request.POST.get('title'))==0:
        return JsonResponse({"success": False, "error": "Please fill title."})
    else:
        title = request.POST.get('title')

    if 'description' not in request.POST or len(request.POST.get('description'))==0:
        return JsonResponse({"success": False, "error": "Please fill description."})
    else:
        description = request.POST.get('description')

    if 'tags' not in request.POST or len(request.POST.get('tags'))==0:
        tags = []
    else:
        tags = json.loads(request.POST.get('tags'))
        tags = [tags]

    if 'problem_image' not in request.FILES:
        return JsonResponse({"success": False, "error": "Please upload images."})
    else:
        file_obj = request.FILES.get('problem_image', None)
        if file_obj == None:
            return JsonResponse({"success": False, "error": "Please upload images."})
     
        file_name = 'images/temp_file-%d.jpg' % random.randint(0,10000000)
        file_full_path = os.path.join(settings.MEDIA_ROOT, file_name)
        dest = open(file_full_path, 'w')
        dest.write(file_obj.read())
        dest.close()

    problem = Problem.objects.create(title=title, user=User.objects.get(id=user_id))
    problem.problem_image = file_name
    problem.description = description
    for tag in tags:
        tag = Tag.objects.get(id=tag)
        problem.tags.add(tag)

    problem.save()

    return JsonResponse({"success": True, "id": problem.id})

@csrf_exempt
def signup(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Please send a post."})

    if 'username' not in request.POST or len(request.POST.get('username'))==0:
        return JsonResponse({"success": False, "error": "Please fill username."})
    else:
        username = request.POST.get('username')

    if 'email' not in request.POST or len(request.POST.get('email'))==0:
        return JsonResponse({"success": False, "error": "Please fill email."})
    else:
        email = request.POST.get('email')

    if 'password'  not in request.POST or len(request.POST.get('password'))==0:
        return JsonResponse({"success": False, "error": "Please fill password."})
    else:
        password = request.POST.get('password')
    
    if User.objects.filter(username__iexact=username).exists():
    	return JsonResponse({"success": False, "error": "This username exists."})
    
    if User.objects.filter(email=email).exists():
        return JsonResponse({"success": False, "error": "This email exists."})
    
    user = User.objects.create(username=username, email=email)    
    user.set_password(password)
    user.save()

    user = authenticate(username=username, password=password)
    django_login(request, user)
    
    return JsonResponse({"success": True, "id": user.id})


@csrf_exempt
def signin(request):
    if request.method != 'POST':
        return JsonResponse({"success": False, "error": "Please send a post."})

    if 'username_or_email' not in request.POST:
        return JsonResponse({"success": False, "error": "Please fill username or email."})
    else:
        username_or_email = request.POST.get('username_or_email')

    if 'password'  not in request.POST:
        return JsonResponse({"success": False, "error": "Please fill password."})
    else:
        password = request.POST.get('password')

    key = 'email__iexact' if '@' in username_or_email else 'username__iexact'
    if User.objects.filter(**{key: username_or_email}).exists():
        user = User.objects.get(**{key: username_or_email})
        user = authenticate(username=user.username, password=password)
        if user is None:
            return JsonResponse({"success": False, "error": "Password incorrect."})
    else:
        return JsonResponse({"success": False, "error": "User do not exists."})

    django_login(request, user)
    if 'remember' not in request.POST:
        request.session.set_expiry(0)
    else:
        request.session.set_expiry(60 * 60 * 24 * 60)

    return JsonResponse({"success": True, "id": user.id})

@csrf_exempt
def profile(request):
    if request.user.is_authenticated():
        return user(request, request.user.id)
    else:
        return user(request, 0)

@csrf_exempt
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

@csrf_exempt
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

@csrf_exempt
def problems_with_user(request, user_id):
    problems = Problem.objects.filter(user__id=user_id)
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

@csrf_exempt
def problem(request, problem_id):
    problem_json = {}
    problem = Problem.objects.get(id=problem_id)
    problem_json['title'] = problem.title
    problem_json['user'] = problem.user.username
    problem_json['problem_image'] = problem.problem_image.url
    problem_json['description'] = problem.description
    problem_json['up'] = problem.up

    return JsonResponse(problem_json)

@csrf_exempt
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
