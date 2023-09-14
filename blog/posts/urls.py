from django.urls import path
from . import views

app_name="posts"

urlpatterns = [
    path('', views.home, name="home_page"),
    path('about/', views.about, name="about_page"),
    path('post/<int:post_id>', views.post_details, name="post_details"),
    path('create_post/', views.create_post, name="create_post")
]