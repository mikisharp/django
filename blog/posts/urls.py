from django.urls import path
from . import views

app_name="posts"

urlpatterns = [
    path('', views.home, name="home_page"),
    path('about/', views.about, name="about_page")
]