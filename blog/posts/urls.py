from django.urls import path
from . import views

app_name="posts"

urlpatterns = [
    path('', views.home, name="home_page"),
    path('about/', views.about, name="about_page"),
    path('post/<int:post_id>', views.post_details, name="post_details"),
    path('create_post/', views.create_post, name="create_post"),
    path('submit_post/', views.submit_post, name="submit_post"),
    path('edit_post/<int:post_id>', views.edit_post, name="edit_post"),
    path('submit_edit_post/<int:post_id>', views.submit_edit_post, name="submit_edit_post"),
    path('delete_post/<int:post_id>', views.delete_post, name="delete_post"),
]