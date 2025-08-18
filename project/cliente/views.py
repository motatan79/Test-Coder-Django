from django.shortcuts import render
from .models import Cliente, Pais

# Create your views here.
def index(request):
    clientes = Cliente.objects.all()
    return render(request, 'cliente/index.html', {'clientes': clientes})
