from django.shortcuts import render
from . import models
from . import forms

# Create your views here.
def index(request):
    return render(request, 'cliente/index.html')

def cliente_list(request):
    clientes = models.Cliente.objects.all()
    context = {
        'clientes': clientes,
    }   
    return render(request, 'cliente/cliente_list.html', context)

def cliente_create(request):
    if request.method == 'GET':
        form = forms.ClienteForm()
        return render(request, 'cliente/cliente_form.html', {'form': form})
 # Implementación de la creación de cliente
