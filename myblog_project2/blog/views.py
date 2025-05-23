from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponseForbidden
from django.contrib.auth.models import User, auth
from django.contrib import messages
from .models import Post, Comment



#Homepage view
def index(request):
    posts = Post.objects.all()
    return render(request, 'index.html', {'posts': posts})


#Register view
# This view handles user registration. It checks if the username and email are already in use, and if not, creates a new user.
def register(request):
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST.get('email')
        password = request.POST['password']
        confirm_password = request.POST.get('confirm_password')

        if password == confirm_password:
            if User.objects.filter(username=username).exists():
                messages.error(request, 'Username already exists')
                return redirect('register')
            
            elif User.objects.filter(email=email).exists():
                messages.error(request, 'Email already in use')
                return redirect('register')
            else: 
                user = User.objects.create_user(username=username, email=email, password=password)
                user.save()
                messages.success(request, 'User created successfully')
                return render(request, 'login.html')
        else:
            messages.error(request, 'Passwords do not match')
            return redirect('register')
    else:
        return render(request, 'register.html')
    

#Login view
def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, 'Login successful')
            return render(request, 'index.html')
        else:
            messages.error(request, 'No user found')
            return redirect('login')
    else:  
        return render(request, 'login.html')
    

#Logout view
def logout_view(request):
        logout(request)
        messages.success(request, 'Logged Out')
        return redirect('index')

#Creat post view
def create_post(request):
    if request.method == 'POST':
        title = request.POST['title']
        content = request.POST['content']
        author = request.user
        if title and content:
            post = Post(title=title, content=content, author=author)
            post.save()
            messages.success(request, 'Post created successfully')
            return redirect('index')
        else:
            messages.error(request, 'Title and content are required')
            return redirect('create_post')
    else:
        return render(request, 'create_post.html')


#Edit post view
def edit_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.user != post.author:
        messages.error(request, 'You can not edit somene else post')
        return redirect('index')


    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')

        if title and content:
            post.title = title 
            post.content = content    
            post.save()
            messages.success(request, 'Post updated successfully')
            return redirect('post', pk=pk)
        else: 
            messages.error(request, 'Title and content are required')
            return redirect('edit_post', pk=pk)
    
    return render(request, 'edit_post.html', {'post': post})

#Delete post view
def delete_post(request, pk):
    post = get_object_or_404(Post, id=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')
        return redirect('index')
    return render(request, 'delete_post.html', {'post': post})


#Post view
def post(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        content = request.POST['content']
        author = request.user
        if author and content:
            comment = Comment(post=post, author=author, content=content)
            comment.save()
            messages.success(request, 'Comment added')
            return redirect('post', pk=pk)
        else:
            messages.error(request, '')
            return redirect('post', pk=pk)
    comments = post.comments.all()
    return render(request, 'post.html', {'post': post, 'comments': comments})




