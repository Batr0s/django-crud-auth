from django.contrib import admin
# Hay que importar la clase que queremos agregar al panel administrador
from .models import Task

# Register your models here.

# Clase para poder mostrar cuándo fue creado
class TaskAdmin(admin.ModelAdmin):
    readonly_fields = ('created', )


# Ahora agregamos Task
admin.site.register(Task, TaskAdmin)


