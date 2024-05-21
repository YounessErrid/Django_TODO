from django.shortcuts import get_object_or_404, redirect, render
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login as auth_login, logout as auth_logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from.models import Todo

# Create your views here.
@login_required(login_url='login')
def index(request):
    if request.method == 'POST':
        title = request.POST['task']
        task_id = request.POST['task_id']
        if title and task_id:
            task = get_object_or_404(Todo, id=task_id)
            task.title = title
            task.save()
            messages.success(request, '👌 Task updated successfully')
            return redirect('home')
        if len(title) == 0:
            messages.error(request, '🤬 Task cannot be empty')
            return redirect('home')
        Todo.objects.create(title=title, author=request.user)
        messages.success(request, '👌 Task created successfully')
        return redirect('home')
    all_tasks = Todo.objects.filter(author=request.user)
    context = {'tasks': all_tasks, 'user': request.user}
    return render(request, 'todoapp/todo.html',  context)
def login(request):
    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get("username", False)  # Assuming username field name is 'username1'
        print(f"Submitted username: {username}")
        password = request.POST.get("password", False) # Assuming password field name is 'password1'
        print(f"Submitted password: {password}")
        user = authenticate( username=username, password=password)
        print (user)
        if user is not None:
            auth_login(request, user)  # Pass only the authenticated user object
            return redirect('home')
        else:
            messages.error(request, 'Email or password is incorrect')
            return redirect('login')
    return render(request, 'todoapp/login.html', {})
def register(request):
    # Check if the user is already logged in
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST['username']
        email = request.POST['email']
        password = request.POST['password']
        if len(password) < 6:
            messages.error(request, 'Password must be at least 6 characters')
            return redirect('register')
        if User.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists')
            return redirect('register')
        if User.objects.filter(email=email).exists():
            messages.error(request, 'Email already exists')
            return redirect('register')
        new_user = User.objects.create_user(username=username, email=email, password=password)
        new_user.save()

        print(new_user)
        return redirect('login')
    return render(request, 'todoapp/register.html', {})
def logout(request):
    auth_logout(request)
    return redirect('login')

@login_required(login_url='login')
def complete_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, author=request.user)
    if not task.comlited :
        task.comlited = True
    else :
        task.comlited = False
    task.save()
    messages.success(request, '👏 Great You Finshed The Task')
    return redirect('home')

@login_required(login_url='login')
def remove_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, author=request.user)
    task.delete()
    messages.success(request, '😥 Task Deleted Successfully')
    return redirect('home')
@login_required(login_url='login')
def edit_task(request, task_id):
    task = get_object_or_404(Todo, id=task_id, author=request.user)
    if request.method == 'POST':
        title = request.POST['task']
        if len(title) == 0:
            messages.error(request, '🤬 Task cannot be empty')
            return redirect('home')
        task.title = title
        task.save()
        messages.success(request, '👌 Task updated successfully')
        return redirect('home')
    context = {'task': task}
    return render(request, 'todoapp/edit_task.html', context)
