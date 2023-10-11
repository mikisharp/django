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
    path('register/', views.register_page, name="register_page"),
    path('login/', views.login_page, name="login_page"),
    path('register_user/', views.register_user, name="register_user"),
    path('login_user/', views.login_user, name="login_user"),
    path('logout_user/', views.logout_user, name="logout_user"),
    path('category_page/', views.category_page, name="category_page"),
    path('add_category/', views.add_category, name="add_category"),
    path('edit_category/<int:item_id>', views.edit_category, name="edit_category"),
    path('delete_category/<int:item_id>', views.delete_category, name="delete_category"),
    path('api/category/', views.category_serializer),
]