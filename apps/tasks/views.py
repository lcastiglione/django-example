from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.http import HttpResponseNotFound
from django.contrib.auth.models import User
from django.contrib.auth import login, logout, authenticate
from django.db import IntegrityError
from .forms.forms import TaskForm
from .models import Task
from django.contrib.auth.decorators import login_required


def home(request):
    return render(request, 'home.html')


def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {'form': UserCreationForm})
    elif request.method == 'POST':
        if request.POST['password1'] == request.POST['password2']:
            # Registrar usuario
            try:
                user = User.objects.create_user(
                    username=request.POST['username'],
                    password=request.POST['password1'])
                user.save()  # Guarda los datos del usuario en la abse de datos
                # Permite crear una sesión para almacenar datos de usuario
                login(request, user)
                return redirect('tasks')
            except IntegrityError:
                return render(request, 'signup.html', {
                    'form': UserCreationForm,
                    'error': 'El usuario ya existe'
                })
        return render(request, 'signup.html', {
            'form': UserCreationForm,
            'error': 'Las contraseñas no coinciden'
        })
    else:
        return HttpResponseNotFound(f"Método '{request.method}' no válido")


def sigout(request):
    logout(request)
    return redirect('home')


def signin(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'form': AuthenticationForm})
    elif request.method == 'POST':
        # Verificar usuario
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        print(user)
        if user is None:
            return render(request, 'login.html', {
                'form': AuthenticationForm,
                'error': 'Usuario o contraseña incorrecta'
            })
        login(request, user)
        return redirect('tasks')
    else:
        return HttpResponseNotFound(f"Método '{request.method}' no válido")


@login_required
def tasks(request):
    tasks = Task.objects.filter(user=request.user)
    return render(request, 'tasks.html', {'tasks': tasks})


@login_required
def create_task(request):
    if request.method == 'GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    elif request.method == 'POST':
        try:
            form = TaskForm(request.POST)
            new_task = form.save(commit=False)
            new_task.user = request.user
            new_task.save()
            return render(request, 'create_task.html', {'form': TaskForm})
        except ValueError:
            return render(request, 'create_task.html', {
                'form': TaskForm,
                'error': 'Por favor, cargar datos válidos'
            })
    else:
        return HttpResponseNotFound(f"Método '{request.method}' no válido")
