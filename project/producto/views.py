from django.shortcuts import render
from django.urls import reverse_lazy
from django.views.generic import ListView, CreateView, UpdateView, DeleteView, DetailView
from .models import *
from .forms import *


# Create your views here.
def index(request):
    return render(request, "producto/index.html", {})

# def productocategoria_list(request):
#     objects = ProductoCategoria.objects.all()
#     context = {"objects_list": objects}
#     return render(request, "producto/productocategoria_list.html", context)

class ProductoCategoriaList(ListView):
    model = ProductoCategoria
    # template_name = "producto/productocategoria_list.html"
    # context_object_name = "objects_list"
    # paginate_by = 10  # Número de elementos por página

    def get_queryset(self):
        if self.request.GET.get('consulta'):
            consultar = self.request.GET.get('consulta')
            object_list = ProductoCategoria.objects.filter(nombre__icontains=consultar)
        else:
            object_list = ProductoCategoria.objects.all()
        return object_list
    
    
class ProductoCategoriaCreate(CreateView):
    model = ProductoCategoria
    form_class = ProductoCategoriaForm
    success_url = reverse_lazy("producto:productocategoria_list")
    
class ProductoCategoriaDetail(DetailView):
    model = ProductoCategoria
    template_name = "producto/productocategoria_detail.html"    
    context_object_name = "object"
    
class ProductoCategoriaUpdate(UpdateView):
    model = ProductoCategoria
    form_class = ProductoCategoriaForm
    success_url = reverse_lazy("producto:productocategoria_list")
    
class ProductoCategoriaDelete(DeleteView):
    model = ProductoCategoria
    success_url = reverse_lazy("producto:productocategoria_list")