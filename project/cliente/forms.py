from django import forms
from . import models 

class ClienteForm(forms.ModelForm):
    class Meta:
        model = models.Cliente
        fields = "__all__" # Puedes especificar los campos que deseas incluir
        # fields = ['nombre', 'apellido', 'email', 'telefono'] # Ejemplo de campos específicos
        # Puedes personalizar los widgets y etiquetas de los campos si es necesario
        # widgets = {
        #     'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        #     'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        # }
        # labels = {
        #     'nombre': 'Nombre',
        #     'apellido': 'Apellido',
        #     'email': 'Correo Electrónico',
        #     'telefono': 'Teléfono',
        # }