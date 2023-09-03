from django.shortcuts import render
from django.http import HttpResponse

# Create your views here.
def home(request):
    #print(request)
    context = {
        'title': 'Home',
        'data': [1,2,3,4,5],
    }
    return render(request, 'home/landingpage.html', context)

def about(request):
    context = {
        'title': 'About',
    }
    return render(request, 'about/about_page.html', context)