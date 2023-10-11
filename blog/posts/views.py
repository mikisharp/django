from django.shortcuts import render, redirect, reverse
from django.http import HttpResponse
from posts.models import (Post, Category)
from posts.forms import *
from django.contrib.auth import (authenticate, login, logout)
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .serializer import *
from rest_framework.response import Response
from rest_framework.decorators import api_view

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

@login_required
def create_post(request):
    categories = Category.objects.order_by('-created_at')
    context = {
        'title': "Add Post",
        'categories': categories
    }
    return render(request, 'post/add_post.html', context)
@login_required 
def submit_post(request):
    # print(request.POST)
    post_title = request.POST.get('title', '')
    subject =request.POST.get('subject', '')
    desc = request.POST.get('description', '')
    category_id = request.POST.get('category')
    main_image = request.FILES.get('main_image', '')
    
    if not post_title:
        messages.error(request, 'Please Add Title')
        return redirect('posts:create_post')
    if not subject:
        messages.error(request, 'Please Add Subject')
        return redirect('posts:create_post')
    if not category_id:
        messages.error(request, 'Please Add Category')
        return redirect('posts:create_post')
    if not desc:
        messages.error(request, 'Please Add Description')
        return redirect('posts:create_post')
    if not main_image:
        messages.error(request, 'Please Add Main image')
        return redirect('posts:create_post')
    category = Category.objects.filter(id=category_id).first()
    if not category:
        messages.error(request, 'Category does not exist')
        return redirect('posts:create_post') 
    
    Post.objects.create (
        title=post_title,
        subject = subject,
        category = category,
        description = desc,
        main_image = main_image,
        author=request.user
    )
    return redirect('posts:home_page')
    
# post_object = Post()
# post_object.title = post_title
# post_object.subject = subject
# post_object.description = desc
# post_object.main_image = main_image
# post_object.save()
    

@login_required
def edit_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    if post:
        context = {
            'post': post,
            'title': 'Edit Post'
        }
        return render(request, 'post/edit_post.html', context)
    return redirect('home_page')

@login_required
def submit_edit_post(request, post_id):
    post = Post.objects.filter(id=post_id).first()
    
    if request.method == "POST":
        post_title = request.POST.get('title', '')
        subject =request.POST.get('subject', '')
        desc = request.POST.get('description', '')
        main_image = request.FILES.get('main_image', '')
        
        if not post_title:
            messages.error(request, 'Please Add Title')
            return redirect('posts:create_post')
        if not subject:
            messages.error(request, 'Please Add Subject')
            return redirect('posts:create_post')
        if not desc:
            messages.error(request, 'Please Add Description')
            return redirect('posts:create_post')
        if not main_image:
            messages.error(request, 'Please Add Main image')
            return redirect('posts:create_post')
        

        Post.objects.filter(id=post_id).update(
            title = post_title,
            subject = subject,
            description = desc,
            main_image = main_image
        )
        
        return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))
    return redirect(reverse('posts:post_details', kwargs={"post_id": post_id}))

@login_required
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
        username = request.POST.get('username', None)
        password = request.POST.get('password')
        
        next_stage = request.GET.get("next")
        
        if not username:
            messages.error(request,"Add username.")
            return redirect('posts:login_page')
        if not password:
            messages.error(request, "Add password")
            return redirect('posts:login_page')
        """ 
        If interested in using Email as a login parameter
        from django.db.models import Q
        user_obj = User.objectss.filter(Q(username=username) | Q(email=username)).first()
        user =authenticate(username=user_ob.username, password=password)
        """
        user =authenticate(username=username, password=password)
        if user:
            login(request, user)
            messages.info(request, f"You are now logged in as {username}.")
            return redirect("posts:home_page" if not next_stage else next_stage)
        else:
            messages.error(request, "Invalid username or password")
            return redirect('posts:login_page')
        
        
    return redirect('posts:login_page')

def logout_user(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('posts:home_page')

@login_required
def category_page(request):
    categories = Category.objects.order_by('-created_at')
    ctxt = {
        'title': "Categories",
        'categories': categories
    }
    return render(request, 'category/category_page.html', ctxt)

def add_category(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        if not name:
            messages.error(request, "Please Add Name")
            return redirect('posts:category_page')
        if Category.objects.filter(name=name).exists():
            messages.error(request, "The category exist")
            return redirect('posts:category_page')
        Category.objects.create(
            name=name
        )
        messages.success(request, 'Category Added Successfully')
        
    return redirect('posts:category_page')

def edit_category(request, item_id):
    if request.method == 'POST':
        name = request.POST.get('name')
        category = Category.objects.filter(id=item_id).first()
        if not name:
            messages.error(request, "Please Add Name")
            return redirect('posts:category_page')
        if not category:
            messages.error(request, "Category not found")
            return redirect('posts:category_page')
        if Category.objects.filter(name__iexact=name).exclude(id=item_id).exists(): 
            messages.error(request, "The category exist")
            return redirect('posts:category_page')
        Category.objects.filter(id=item_id).update(
            name=name
        )
        messages.success(request, 'Category Updated Successfully')
        
    return redirect('posts:category_page')

def delete_category(request, item_id):
    category = Category.objects.filter(id=item_id).first()
    if not category:
            messages.error(request, "Category not found")
            return redirect('posts:category_page')
    category.delete()
    messages.success(request, 'Category Deleted Successfully') 
    return redirect('posts:category_page')  
    
@api_view(['GET'])
def category_serializer(request):
    categories = Category.objects.order_by('-created_at')
    category_serializer = CategorySerializer(categories, many=True)
    return Response(category_serializer.data, status=200)
    