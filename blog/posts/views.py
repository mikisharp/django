from django.shortcuts import render
from django.http import HttpResponse
from posts.models import Post


# Create your views here.
def home(request):
    posts = Post.objects.all()
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

