from django.shortcuts import render, HttpResponse, HttpResponseRedirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, authenticate
from problems.models import Problem
from comments.models import Comment
from django.contrib.auth.models import User
from favorite.models import Favorite
from tags.models import Tag
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from django.utils import timezone
import json, os, random
import datetime
import time

DIS = 10000

def get_problems_json(user, problems):
    problems_json = []
    for problem in problems:
        problem_json = {}
        problem_json['id'] = problem.id
        problem_json['title'] = problem.title
        problem_json['user'] = problem.user.username
        problem_json['problem_image'] = problem.problem_image.url
        problem_json['description'] = problem.description
        problem_json['up'] = problem.up
        comments = Comment.objects.filter(problem=problem)  
        comments_json = []
        for comment in comments:
            comments_json.append(comment.id)
        problem_json['comments'] = comments_json
        if problem.create_at:
            problem_json['create_at'] = problem.create_at.strftime('%Y-%m-%d')
        else:
            problem_json['create_at'] = '1970-1-1'
        if user is not None and user.favorite_set.filter(problem=problem).exists():
            problem_json['is_favorite'] = True
        else:
            problem_json['is_favorite'] = False
        problems_json.append(problem_json)

    return problems_json

@csrf_exempt
def problems_around(request):
    if 'X' in request.GET:
        value = request.GET.get('X')
        if '.' in value:
            value = value[:value.find('.')]
        x = int(value) * 100
    else:
        return JsonResponse({"success": False, "error": 'please fill X field.'})

    if 'Y' in request.GET:
        value = request.GET.get('Y')
        if '.' in value:
            value = value[:value.find('.')]
        y = int(value) * 100
    else:
        return JsonResponse({"success": False, "error": 'please fill Y field.'})

    last_time = timezone.now() - datetime.timedelta(hours=1)
    problems = Problem.objects.all()
    problems = [problem for problem in problems
                if problem.create_at.replace(tzinfo=None) > last_time.replace(tzinfo=None)]

    problem_list = []
    for problem in problems:
        if problem.x:
            xx = problem.x
        else:
            xx = 0
        if problem.y:
            yy = problem.y
        else:
            yy = 0

        if abs(xx - x) < dis and abs(yy -y) < DIS:
            problem_list.append(problem)

    problems_json = get_problems_json(user, problem_list.reverse())
    return JsonResponse(problems_json)


@csrf_exempt
def JsonResponse(params):
    return HttpResponse(json.dumps(params))

@csrf_exempt
def up(request, problem_id):
    problem = get_object_or_404(Problem, id=problem_id)
    problem.up += 1
    problem.save()
    return JsonResponse({"success": True, "id": problem_id})

@csrf_exempt
def myfavorite(request, user_id):
    user = None
    user = get_object_or_404(User, id=user_id)

    problems_json = {}
    if user:
        problems = [favorite.problem for favorite in user.favorite_set.all()]
        problems_json = get_problems_json(user, problems)

    return JsonResponse(problems_json)

@csrf_exempt
def is_favorite(request):
    user, problem = None, None
    if 'problem_id' in request.GET:
        problem = get_object_or_404(Problem, id=request.GET.get('problem_id'))
    if 'user_id' in request.GET:
        user = get_object_or_404(User, id=request.GET.get('user_id'))

    if user and problem:
        favorite = user.favorite_set.filter(problem=problem)
        if favorite.exists():
            return JsonResponse({"is_favorite": True})
        else:
            return JsonResponse({"is_favorite": False})

    return JsonResponse({"is_favorite": False})

@csrf_exempt
def unfavorite(request):
    user, problem = None, None
    if 'problem_id' in request.GET:
        problem = get_object_or_404(Problem, id=request.GET.get('problem_id'))
    if 'user_id' in request.GET:
        user = get_object_or_404(User, id=request.GET.get('user_id'))

    if user and problem:
        favorite = user.favorite_set.filter(problem=problem)
        if favorite.exists():
            favorite.delete()
        return JsonResponse({"result": "unfavorite success."})

    return JsonResponse({"result": "Not found problem or user."})

@csrf_exempt
def favorite(request):
    user, problem = None, None
    if 'problem_id' in request.GET:
        problem = get_object_or_404(Problem, id=request.GET.get('problem_id'))
    if 'user_id' in request.GET:
        user = get_object_or_404(User, id=request.GET.get('user_id'))

    if user and problem:
        favorite, create = Favorite.objects.get_or_create(user=user, problem=problem)
        return JsonResponse({"result": "Like success."})

    return JsonResponse({"result": "Not found problem or user."})

@csrf_exempt
def post_profile(request, user_id):
    user = User.objects.get(id=user_id)
    profile = user.profile
    if 'username' in request.POST:
        user.username = request.POST.get('username')
        user.save()

    if 'email' in request.POST:
        user.email = request.POST.get('email')
        user.save()

    if 'birthday' in request.POST:
        str = request.POST.get('birthday')
        profile.birthday = datetime.datetime.strptime(str,'%Y-%m-%d')

    if 'description' in request.POST:
        profile.description = request.POST.get('description')
 
    file_obj = None
    if 'profile_image' in request.FILES:
        file_obj = request.FILES.get('profile_image')
        file_obj = file_obj.read()
    elif 'profile_image' in request.POST:
        file_obj = request.POST.get('profile_image') #.decode('hex')
   
    if file_obj is None:
        try:
            file_obj = request.FILES[0]
        except:
            pass
 
    if file_obj is not None:
        file_name = 'images/temp_file-%d.jpg' % random.randint(0,100000000)
        file_full_path = os.path.join(settings.MEDIA_ROOT, file_name)
        dest = open(file_full_path, 'wb')
        dest.write(file_obj)
        dest.close()
        profile.profile_image = file_name

    profile.save()
    return JsonResponse({'success': True, 'id': user.id})

@csrf_exempt
def userprofile(request, user_id):
    user = User.objects.get(id=user_id)
    user_json = {}
    user_json['id'] = user.id
    user_json['username'] = user.username
    user_json['email'] = user.email
    profile = user.profile
    if profile.birthday is not None:
        user_json['birthday'] = profile.birthday.strftime('%Y-%m-%d')
    else:
        user_json['birthday'] = ''

    if profile.description is not None:
        user_json['description'] = profile.description
    else:
        user_json['description'] = ''

    try:
        user_json['profile_image'] = profile.profile_image.url
    except:
        user_json['profile_image'] = ''

    return JsonResponse(user_json)
    
@csrf_exempt
def post_comment(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Please send a post."})

    if 'user_id' not in request.POST or len(request.POST.get('user_id'))==0:
        return JsonResponse({"success": False, "error": "Please login first."})
    else:
        user_id = request.POST.get('user_id')
        user = User.objects.get(id=user_id)

    if 'reply_user_id' not in request.POST or len(request.POST.get('reply_user_id'))==0:
        reply_user = None
    else:
        user_id = request.POST.get('reply_user_id')
        reply_user = User.objects.get(id=user_id)

    if 'problem_id' not in request.POST or len(request.POST.get('problem_id'))==0:
        return JsonResponse({"success": False, "error": "Please comment a problem."})
    else:
        problem_id = request.POST.get('problem_id')
        problem = Problem.objects.get(id=problem_id)
        
    comment = Comment.objects.create(user=user, problem=problem)
    comment.reply_user = reply_user
    comment.description = request.POST.get('description', '')

    return JsonResponse({"success": True, "id": comment.id})

@csrf_exempt
def post_tag(request):
    if request.method != "POST":
        return JsonResponse({"success": False, "error": "Please send a post."})
    
    if 'tag_name' not in request.POST or len(request.POST.get('tag_name'))==0:
        return JsonResponse({"success": False, "error": "Please fill tag name."})
    else:
        tag_name = request.POST.get('tag_name')

    tag = Tag.objects.create(name=tag_name)
    tag.description = request.POST.get('description', '')
    tag.save()
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

    if 'X' in request.POST:
        value = request.POST.get('X')
        if '.' in value:
            value = value[:value.find('.')]
        X = int(value) * 100
    else:
        X = 0

    if 'Y' in request.POST:
        value = request.POST.get('Y')
        if '.' in value:
            value = value[:value.find('.')]
        Y = int(value) * 100
    else:
        Y = 0

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
    problem.x = X
    problem.y = Y
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
def problems(request, user_id):
    user = None
    try:
        user = User.objects.get(id=user_id)
    except:
        user = None

    problems = Problem.objects.all()
    problems_json = get_problems_json(user, problems)
    return JsonResponse(problems_json)

@csrf_exempt
def problems_with_user(request, user_id):
    user = get_object_or_404(User, id=user_id)
    problems = Problem.objects.filter(user__id=user_id)
    problems_json = get_problems_json(user, problems)
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

    comments = Comment.objects.filter(problem=problem)
    comments_json = []
    for comment in comments:
        comments_json.append(comment.id)
    problem_json['comments'] = comments_json
    problem_json['create_at'] = problem.create_at.strftime('%Y-%m-%d')

    return JsonResponse(problem_json)

@csrf_exempt
def comments_with_problem(request, problem_id):
    comments_json = []
    comments = Comment.objects.filter(problem__id=problem_id)
    for comment in comments:
        comment_json = {}
        comment_json['id'] = comment.id
        comment_json['user'] = comment.user.username
        comment_json['reply_user'] = comment.reply_user.username
        comment_json['user_id'] = comment.user.id
        comment_json['reply_user_id'] = comment.reply_user.id
        comment_json['problem'] = comment.problem.title
        comment_json['description'] = comment.description

        comments_json.append(comment_json)
    
    return JsonResponse(comments_json)
