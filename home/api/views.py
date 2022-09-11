from django.shortcuts import redirect
from django.http import JsonResponse, HttpResponseBadRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from ..models import BlogComment, Post, Contact
import requests
import json
from decouple import config

def get_api_routes(request):
    routes = [
        {
            'method': 'post',
            'route': '/api/signup',
            'description': 'This api will create a new user in the database'
        },
        {
            'method': 'post',
            'route': '/api/login',
            'description': 'This api will authenticate and login a user'
        },
        {
            'method': 'get',
            'route': '/api/logout',
            'description': 'This api will log out a logged in user'
        },
        {
            'method': 'post',
            'route': '/api/delete_account',
            'description': 'This api will delete a specific user from the database'
        },
        {
            'method': 'post',
            'route': '/api/postcomment',
            'description': 'This api will create a new comment/reply against the corresponding blogpost'
        },
        {
            'method': 'post',
            'route': '/api/contact',
            'description': 'This api will create a new contact information'
        }
    ]
    return JsonResponse({ 'routes': routes }, safe=False)

def user_signup(request):
    if request.method == "POST":
        username = request.POST.get('signupUserName')
        password = request.POST.get('signupPassword1')
        cpassword = request.POST.get('signupPassword2')
        path = request.POST.get('path')

        if not username or not password or not cpassword:
            messages.error(request, "Please fill up your signup credentials!")
            return redirect(path)
        
        elif len(username) < 6 or len(username) > 12:
            messages.error(request, "Username must be between 6 to 12 characters!")
            return redirect(path)
        
        elif str(username).isalpha() or str(username).isnumeric() or not str(username).isalnum():
            messages.error(request, "Username must contain only aphanumeric characters!")
            return redirect(path)

        elif User.objects.filter(username=username).first():
            messages.error(request, "This user already exists!")
            return redirect(path)

        elif len(password) < 8:
            messages.error(request, "Password must contain atleast 8 characters!")
            return redirect(path)

        elif str(password).isalpha() or str(password).isnumeric() or str(password).isalnum():
            messages.error(request, "Password must contain alphanumeric as well as special characters!")
            return redirect(path)

        elif (password!= cpassword):
            messages.error(request, "Password and confirm password do not match!")
            return redirect(path)

        else:
            newUser = User.objects.create_user(username, None, password)
            newUser.save()
            messages.success(request, "Your new user account has been created sucessfully!")
            return redirect(path)
    else:
        return HttpResponseBadRequest(f"<h1>Bad Request (400)</h1><p>{request.method} method is not allowed!</p>")

def user_login(request):
    if request.method == "POST":
        username = request.POST.get('loginUserName')
        password = request.POST.get('loginPassword')
        path = request.POST.get('path')
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            messages.success(request, "You have been successfully logged in!")
            return redirect(path)
        else:
            messages.error(request, "Please provide valid credentials!")
            return redirect(path)
    else:
        return HttpResponseBadRequest(f"<h1>Bad Request (400)</h1><p>{request.method} method is not allowed!</p>")

def user_logout(request):
    if request.user.is_authenticated:
        logout(request)
        messages.success(request, "Please fill up your signup credentials!")
        return redirect('/')
    else:
        return HttpResponse('<h1>Unauthorized (401)</h1>', status=401)

def post_comment(request):
    if request.method == "POST":
        user = request.user
        comment = request.POST.get('comment')
        slug = request.POST.get('slug')
        parentSno = request.POST.get('parentSno')
        path = request.POST.get('path')
        post = Post.objects.filter(slug=slug).first()

        if not comment:
            messages.error(request, "Please enter a comment!")
            return redirect(path)
        else:
            if parentSno == "":
                newComment = BlogComment(comment=comment, post=post, user=user)
                newComment.save()
                messages.success(request, "Your comment has been added successfully!")
                return redirect(path)
            else:
                parent = BlogComment.objects.filter(sno=parentSno).first()
                newComment = BlogComment(comment=comment, post=post, user=user, parent=parent)
                newComment.save()
                messages.success(request, "Your reply has been added successfully!")
                return redirect(path)

def contact(request):
    if request.method == "POST":
        name = request.POST.get("name")
        email = request.POST.get("email")
        phone = request.POST.get("phone")
        message = request.POST.get("message")
        clientKey = request.POST['g-recaptcha-response']
        secretKey = config('RECAPTCHA_SECRET')

        captchaData = {
            "secret": secretKey,
            "response": clientKey
        }
        r = requests.post('https://www.google.com/recaptcha/api/siteverify', data=captchaData)
        response = json.loads(r.text)
        verifyStatus = response['success']

        if not name or not email or not phone or not message:
            messages.error(request, "Please fill your contact details!")
            return redirect('/contact')

        elif len(name) < 5 or len(email) < 7 or len(phone) < 10 or len(message) < 10:
            messages.error(request, "Please the form correctly!")
            return redirect('/contact')

        elif not verifyStatus:
            messages.error(request, "Invalid reCAPTCHA! Please try again.")
            return redirect('/contact')

        else:
            newContact = Contact(name=name, email=email, phone=phone, message=message)
            newContact.save()
            messages.success(request, "Your contact form has been submitted successfully!")
            return redirect('/contact')
    else:
        return HttpResponseBadRequest(f"<h1>Bad Request (400)</h1><p>{request.method} method is not allowed!</p>")