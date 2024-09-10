from django.db import models
from django.contrib.auth.models import User

# Create your models here.
# Creamos clases que serviran como tablas en una base de datos
# Recuerda que después de modificar o crear tablas hay que ejecutar los comandos:
# 'python manage.py makemigrations'
# 'python manage.py migrate'

class Task(models.Model):
    title = models.CharField(max_length=100)
    # blank True, el campo es opcional y puede dejarse en blanco
    description = models.TextField(blank=True)
    # auto_now_add almacena automáticamente la fecha y hora en que se crea
    created = models.DateTimeField(auto_now_add=True)
    # campo opcional, puede ser null
    datecompleted = models.DateTimeField(null=True, blank=True)
    # Valor predeterminado False
    important = models.BooleanField(default=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title + ' - by ' + self.user.username

# La clase user ya viene por defecto en Django, hay que importarla
# class User()

