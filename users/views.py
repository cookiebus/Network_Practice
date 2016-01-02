from django.shortcuts import render, HttpResponseRedirect
from ratelimit.decorators import ratelimit
from django.contrib.auth.models import User
from django.contrib.auth import login as django_login, authenticate
from users.forms import (
    SignupForm,
    SigninForm
)

# Create your views here.
@ratelimit(key='post:email', rate='10/m', block=True)
def signup(request):
    if request.method != "POST":
        signup_form = SignupForm()
        return render(request, "users/signup.html", locals())

    signup_form = SignupForm(request.POST)
    if signup_form.is_valid():
        email = signup_form.cleaned_data['email']
        username = signup_form.cleaned_data['username']
        password = signup_form.cleaned_data['password']

        if User.objects.filter(username__iexact=username).exists():
            errors = signup_form._errors.setdefault("username", ErrorList())
            errors.append(u"Already Exists")
            return render(request, "account/signup.html", locals())

        user = signup_form.save(commit=False)
        user.set_password(password)
        user.save()

        user = authenticate(username=username, password=password)
        django_login(request, user)
        next = request.GET.get('next', '')
        if next == '':
            next = '/'
        return HttpResponseRedirect(next)

    return render(request, "users/signup.html", locals())

@ratelimit(key='post:email', rate='10/m', block=True)
def signin(request):
    next = request.GET.get('next', '')

    signin_form = SigninForm()
    if request.method != 'POST':
        return render(request, 'users/signin.html', locals())

    signin_form = SigninForm(request.POST)
    if not signin_form.is_valid():
        login_errors = True
        return render(request, 'users/signin.html', locals())

    username_or_email = signin_form.cleaned_data['username_or_email']
    password = signin_form.cleaned_data['password']

    key = 'email__iexact' if '@' in username_or_email else 'username__iexact'
    if User.objects.filter(**{key: username_or_email}).exists():
        user = User.objects.get(**{key: username_or_email})
        user = authenticate(username=user.username, password=password)
        if user is None:
            login_errors = True
            return render(request, 'users/signin.html', locals())
    else:
        login_errors = True
        return render(request, 'users/signin.html', locals())

    django_login(request, user)

    if 'remember' not in request.POST:
        request.session.set_expiry(0)
    else:
        request.session.set_expiry(60 * 60 * 24 * 60)

    next = request.GET.get('next', '')
    if next == '':
        next = '/'
    return HttpResponseRedirect(next)
