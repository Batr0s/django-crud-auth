from django.shortcuts import render, redirect, get_object_or_404
# UserCreationForm es el formulario de registro de usuarios predeterminado de Django
# AuthenticationForm para comprobar que el usuario existe
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
# User permite registrar usuarios (signup)
from django.contrib.auth.models import User
# login crea una cookie con los datos del user
# logout elimina la cookie de sesión
# Autentica el nombre de usuario y password
from django.contrib.auth import login, logout, authenticate
# IntegrityError sirve para controlar errores de usernames ya existentes
from django.db import IntegrityError
# TaskForm es el formulario creado a partir de la clase Task
from .forms import TaskForm
# Importamos Task usando el modulo models porque es una manera de interactuar con la base de datos
from .models import Task
from django.utils import timezone
# PROTEGER RUTAS con login_required. Redirige a login, pero hay que especificarle donde está el login en settings.py
from django.contrib.auth.decorators import login_required

# from django.http import HttpResponse

# Create your views here.
# Esta forma de pasar el contenido html no es escalable, por eso creamos la carpeta 'templates' y ahí sí que creamos el archivo html
# def hello_world(request):
#     return HttpResponse('<h1>Hello world</h1>')

def home(request):
    return  render(request, 'home.html')

def signup(request):

    if request.method =='GET':
        print('Obteniendo datos.') 
        return  render(request, 'signup.html', {'form': UserCreationForm})
    
    else:
        print(request.POST)
        print('Enviando  datos.')
        if request.POST['password1'] == request.POST['password2']:
            try:
                # register user
                user = User.objects.create_user(username=request.POST['username'], password=request.POST['password1'])
                user.save()
                login(request, user)
                # Redirect crea una nueva solicitud http. Además cambia la url, cosa que render no hace.
                # El parámetro de redirect es un string con el name de la ruta (urls.py)
                return redirect('tasks')
            except IntegrityError:
                return  render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Username already exist'})
        return  render(request, 'signup.html', {'form': UserCreationForm, 'error': 'Passwords do not match'})

# login_required para proteger la url
@login_required
def tasks(request):
    # Contiene todas las tareas
    # tasks = Task.objects.all()
    
    # Filtramos por las tareas del usuario actual y por tareas incompletas 'datecompleted' está en models.py
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=True)
    return render(request, 'tasks.html', {'tasks': tasks})

@login_required
def tasks_completed(request):
    # datecompleted__isnull en False para mostrar las completadas. -datecompleted para mostrar las últimas completadas
    tasks = Task.objects.filter(user=request.user, datecompleted__isnull=False).order_by('-datecompleted')
    return render(request, 'tasks.html', {'tasks': tasks})

# signout y no logout porque es una palabra clave
@login_required
def signout(request):
    # sale de la sesión y elimina la cookie de sesión creada con user en la funcion signup
    logout(request)
    # redirect usa el name de la ruta como parámetro
    return redirect('home')

def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {'form': AuthenticationForm})
    else:
        print(request.POST)
        user = authenticate(request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            print(user)
            return render(request, 'signin.html', {'form': AuthenticationForm, 'error': 'Username or password is incorrect'})
        else:
            # Para hacer login también se guarda la información de sesión en una cookie
            login(request, user)
            return redirect('tasks')

@login_required
def create_task(request):

    if request.method =='GET':
        return render(request, 'create_task.html', {'form': TaskForm})
    else:
        try:
            # form es el html del formulario TaskForm
            form = TaskForm(request.POST)
            # new_task contiene los valores del formulario create_task
            new_task = form.save(commit=False)
            # Ahora le agregamos el usuario
            new_task.user = request.user
            # Guardamos la task (se puede ver dentro del panel admin)
            new_task.save()
            return redirect('tasks')
        except:
            return render(request, 'create_task.html', {'form': TaskForm, 'error': 'Please, provide valid data'})

# task_id debe ser igual al nombre usado en urls.py
@login_required
def task_detail(request, task_id):
    # Esta es una manera, pero en casdo de buscar con un id que no existe, te tumba el servidor.
    # task = Task.objects.get(pk=task_id)

    if request.method == 'GET':
        # Con get_object_404 ya no tumba el server sino que muestra un error 404
        task = get_object_or_404(Task, pk=task_id, user=request.user)
        form = TaskForm(instance=task)
        return render(request, 'task_detail.html', {'task':task, 'form':form})
    else:
        try:
            task = get_object_or_404(Task, pk=task_id, user=request.user)
            form = TaskForm(request.POST, instance=task)
            form.save()
            return redirect('tasks')
        except ValueError:
            return render(request, 'task_detail.html', {'task':task, 'form':form, 'error': 'Error updating task'})

@login_required
def complete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        # datecompleted es un campo de la BD en models.py
        task.datecompleted = timezone.now()
        task.save()
        return redirect('tasks')

@login_required
def delete_task(request, task_id):
    task = get_object_or_404(Task, pk=task_id, user=request.user)
    if request.method == 'POST':
        task.delete()
        return redirect('tasks')


