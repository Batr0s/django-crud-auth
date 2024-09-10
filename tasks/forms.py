# Este archivo sirve para crear tus propios formularios
# ModelForm es una clase que permite extenderla
from django import forms 
from .models import Task

class TaskForm(forms.ModelForm):
    class Meta:
        # Le decimos que el formulario que crearé estará basado en la clase Task
        model = Task
        # ESpecificamos los campos que queremos utilizar
        fields = ['title', 'description', 'important']
        # widgets sirve en este caso para agregar un atributo 'class' con un valor 'form-control' al input 'title'
        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Write a title'}),
            'description': forms.Textarea(attrs={'class': 'form-control', 'placeholder': 'Write a description'}),
            # 'important': forms.CheckboxInput(attrs={'class': 'form-check-input m-auto'}),
        }

# Para usar este formulario hay que importarlo dentro del archivo views.py