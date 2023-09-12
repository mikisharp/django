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