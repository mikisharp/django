from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from posts.models import Post
from posts.forms import *
from django.contrib.auth import (authenticate, login)

# Create your views here.
def home(request):
    posts = Post.objects.order_by("-created_at")
    #print(request)
    context = {
        'title': 'Home',
        'posts': posts
    }
    
    return render(request, 'home/landingpage.html', context)
 
def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'about/about_page.html', context)

def post_details(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    print(post)
   
    context = {
        "post": post,
        "title": post.title
    }
    return render(request, 'post/single_post.html', context)

def create_post(request):
    context = {
        'title': "Add Post"
        
    }
    return render(request, 'post/add_post.html')

def submit_post(request):
    # print(request.POST)
    post_title = request.POST.get('title', '')
    subject =request.POST.get('subject', '')
    desc = request.POST.get('description', '')
    main_image = request.FILES.get('main_image', '')
      
    # Post.objects.create (
    #     title=post_title,
    #     subject = subject,
    #     description = desc,
    #     main_image = main_image,
    # )
    
    # post_object = Post()
    # post_object.title = post_title
    # post_object.subject = subject
    # post_object.description = desc
    # post_object.main_image = main_image
    # post_object.save()
    print(request.method)
    if request.method == 'POST':
        post_form = PostForm(request.POST)
        if post_form.is_valid():
            post_form.save()
            return redirect('post:home_page')
        else:
            # print(post_form.errors)
            context = {
                'title': "Add post",
                'form': post_form
            }
            return render(request, 'post/add_post.html', context)
        
    return redirect('posts:create_post')


def edit_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post:
        context = {
            'post': post,
            'title': 'Edit Post'
        }
        return render(request, 'post/edit_post.html', context)
    return redirect('home_page')


def submit_edit_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    
    if request.method == "POST":
        # print(request.POST)
        # post_title = request.POST.get('title', '')
        # subject =request.POST.get('subject', '')
        # desc = request.POST.get('description', '')
        # main_image = request.FILES.get('main_image', '')
        
        
        # post.title = post_title
        # post.subject = subject
        # post.description = desc
        # post.main_image = main_image
        # post.save()
        # Post.objects.filter(id=post_id).update(
        #     title = post_title,
        #     subject = subject,
        #     description = desc,
        #     main_image = main_image
        # )
        
        post_form = PostForm(request.POST, instance=post)
        if post_form.is_valid():
            post_form.save()
            return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))
        else:
            context = {
                'post': post,
                'title': 'Edit Post',
                'form': post_form
            }
            return render(request, 'post/edit_post.html', context)
    return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))


def delete_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post:
        post.delete()
        return redirect('posts:home_page')

def register_page(request):
    context = {
        'title': 'Register'
    }
    return render(request, 'auth/register.html', context)
    
def login_page(request):
    context = {
        'title': 'Login'
    }
    return render(request, 'auth/login.html', context)

def register_user(request):
    if request.method == "POST":
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            user_form.save()
            return redirect('posts:login_page')
        else:
            context = {
                'title': 'Register',
                'form': user_form,
            }
            return render(request, 'auth/register.html', context)
    return redirect('posts:register_page')

def login_user(request):
    if request.method == "POST":
        user_form = UserLoginForm(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        if user_form.is_valid():
            user_obj = authenticate(username=username, password=password)
            login(request, user_obj)
            return redirect('post:home_page')
        else:
            context = {
                'title': 'Login',
                'form': user_form,
            }
            return render(request, 'auth/login.html', context)
    return redirect('posts:login_page')