from django.shortcuts import render
from . import models

# Create your views here.
def index(request):
    return render(request, 'cliente/index.html')

def cliente_list(request):
    clientes = models.Cliente.objects.all()
    context = {
        'clientes': clientes,
    }   
    return render(request, 'cliente/cliente_list.html', context)
