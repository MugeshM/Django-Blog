from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.http import HttpResponse,HttpResponseRedirect
from .models import Blogpost,Blogcomments,Account
from django.utils import timezone
from app.newblogapp.serializers import SignupSerializer, LoginSerializer
from django.contrib.auth import authenticate, login as auth_login
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import logout
import json

@login_required
def index(request):
    latest_posts = Blogpost.objects.order_by('-posted_date')[:10]
    context = {'latest_posts': latest_posts}
    return render(request, 'myblog/index.html', context)

# @login_required
# def index(request):
#     return Response("Hello");

@login_required
def detail(request,blogpost_id):
        blogpost=Blogpost.objects.get(pk=blogpost_id)
        context = {"blogpost":blogpost}
        return render(request, 'myblog/postdetail.html', context)

@login_required
def post(request):
    try:
        #author_name = request.POST['author_name']
        author_name=request.user.first_name
        article_title = request.POST['article_title']
        article_content= request.POST['article_content']
    except:
        return render(request, 'myblog/newpost.html', {
            'error_message': "Error posting your article.",
        })
    else:
        query=Blogpost(post_title=article_title,post_text=article_content,author_name=author_name,posted_date=timezone.now())
        query.save()
        return HttpResponseRedirect("/blog/")

@login_required
def postcomment(request,blogpost_id):
    try:
        #comm_name=request.POST['comm_name']
        comm_name=request.user.first_name
        comm_text=request.POST['comm_content']
    except:
        return render(request, 'myblog/postdetail.html', {
            'error_message':"Error posting your comment.",
        })
    else:
        query = Blogpost.objects.get(pk=blogpost_id)
        query.blogcomments_set.create(comment_name=comm_name,comment=comm_text,postid=blogpost_id,comment_date=timezone.now())
        return HttpResponseRedirect("/blog/"+blogpost_id)

@login_required
def newpost(request):
    return render(request, "myblog/newpost.html")

def login(request):
    return render(request, "myblog/login.html")

@api_view(['POST'])
@permission_classes((AllowAny,))
def logincheck(request):
    try:
        user_name=request.POST['user_name']
        user_pass=request.POST['user_pass']
    except:
         return render(request, 'myblog/login.html', {
            'error_message':"Error logging in.",
        })
    else:
        # cnt=Account.objects.filter(first_name=user_name,password=user_pass).count()
        account = authenticate(email=user_name, password=user_pass)
        print account
        print user_name,user_pass
        if account is not None:
            auth_login(request, account)
            serialized = LoginSerializer(account)
            return index(request)
        else:
            return render(request, 'myblog/login.html', {
            'error_message':"Username/password is incorrect.",
            })

def logout_view(request):
    logout(request)
    return render(request, "myblog/login.html")

def signup(request):
    return render(request, "myblog/signup.html")

# def signupcheck(request):
#     try:
#         user_name = request.POST['user_name']
#         user_pass = request.POST['user_pass']
#         user_conpass= request.POST['user_conpass']
#         user_email=request.POST['user_email']
#     except:
#         return render(request, 'myblog/signup.html', {
#             'error_message': "Error posting your article.",
#         })
#     else:
#       if(user_pass==user_conpass):
#         userflag=Account.objects.filter(username=user_name).count()
#         if(userflag==0):
#             query=Account(createdate=timezone.now(),username=user_name,userpass=user_pass,useremail=user_email)
#             query.save()
#             return render(request, 'myblog/login.html', {
#                 'success_message': "Account Created successfully. You can login now",
#             })
#         else:
#             return render(request, 'myblog/signup.html', {
#                 'error_message': "Username already exists. Please choose different one",
#             })
#       else:
#          return render(request, 'myblog/signup.html', {
#             'error_message': "Password && confirm password Doesn't match. Try Again",
#         })

@permission_classes((AllowAny,))
def signupcheck(request):
    if request.method == 'POST':
        print request.POST
        print request.POST["email"]
        # data = JSONParser().parse(request)
        serializer = SignupSerializer(data=request.POST)

        if not serializer.is_valid():
            # return Response(serializer.errors,\
            #                 status=status.HTTP_400_BAD_REQUEST)
            userflag=Account.objects.filter(email= request.POST['email']).count()
            if(userflag!=0):
                return render(request, 'myblog/signup.html', {
                    'error_message': "Username already exists. Please choose different one",
                })
            return render(request, 'myblog/signup.html', {
                     'error_message': "Problem Creating Account. Try Again",
             })
        else:
                user = serializer.save()
                output_serializer = SignupSerializer(user)
                return render(request, 'myblog/login.html', {
                    'success_message': "Account Created successfully. You can login now",
                })


def session_lost(request):
    return render(request, 'myblog/login.html', {
            'error_message':"Session not found. Please Login",
            })