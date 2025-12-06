from django import forms
from .models import Equipo, Perfil


class EquipoForm(forms.ModelForm):
    class Meta:
        model = Equipo
        fields = ['nombre', 'pais', 'logo']

class PerfilForm(forms.ModelForm):
    class Meta:
        model = Perfil
        fields = ['equipo']
from django import forms
from . import models 

POSICIONES = [
    ('Portero', 'Portero'),
    ('Defensa', 'Defensa'),
    ('Medio', 'Medio'),
    ('Delantero', 'Delantero'),
]

class ClienteForm(forms.ModelForm):
    posicion1 = forms.ChoiceField(choices=POSICIONES, required=True, label='Posición Principal')
    posicion2 = forms.ChoiceField(choices=POSICIONES, required=True, label='Posición Secundaria')

    def clean(self):
        cleaned_data = super(ClienteForm, self).clean()
        pos1 = cleaned_data.get('posicion1')
        pos2 = cleaned_data.get('posicion2')
        if pos1 and pos2 and pos1 == pos2:
            self.add_error('posicion2', 'La posición secundaria debe ser diferente a la principal.')
        return cleaned_data

    class Meta:
        model = models.Cliente
        # Limitar a los campos que mostramos en el formulario de "Agregar jugador"
        fields = ['nombre', 'apellido', 'apodo', 'edad', 'posicion1', 'posicion2']
        #fields = ['nombre', 'apellido', 'email', 'telefono'] # Ejemplo de campos específicos
        #Puedes personalizar los widgets y etiquetas de los campos si es necesario
        # widgets = {
        #     'nombre': forms.TextInput(attrs={'class': 'form-control'}),
        #     'apellido': forms.TextInput(attrs={'class': 'form-control'}),
        #     'email': forms.EmailInput(attrs={'class': 'form-control'}),
        #     # 'telefono': forms.TextInput(attrs={'class': 'form-control'}),
        # }
        # labels = {
        #     'nombre': 'Nombre',
        #     'apellido': 'Apellido',
        #     'email': 'Correo Electrónico',
        #     # 'telefono': 'Teléfono',
        # }


class SeleccionJugadoresForm(forms.Form):
    jugadores = forms.ModelMultipleChoiceField(
        queryset=models.Cliente.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        label="Selecciona 16 jugadores",
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Cambiar choice_label para mostrar nombre + posiciones
        self.fields['jugadores'].label_from_instance = lambda obj: f"{obj.nombre} {obj.apellido} ({obj.posicion1}/{obj.posicion2})"


