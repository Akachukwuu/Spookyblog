from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('register', views.register, name='register'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('create_post', views.create_post, name='create_post'),
    path('post/<str:pk>/', views.post, name='post'),
    path('post/<int:pk>/edit_post/', views.edit_post, name='edit_post'),
    path('post/<int:pk>/delete_post/', views.delete_post, name='delete_post'),
]