from django.shortcuts import render
from django.views.generic import ListView, CreateView, UpdateView, DeleteView
from .models import Producto, ProductoCategoria

# Create your views here.
def index(request):
    return render(request, "producto/index.html", {})

# def productocategoria_list(request):
#     objects = ProductoCategoria.objects.all()
#     context = {"objects_list": objects}
#     return render(request, "producto/productocategoria_list.html", context)

class ProductoCategoriaListView(ListView):
    model = ProductoCategoria
    template_name = "producto/productocategoria_list.html"
    context_object_name = "objects_list"
    paginate_by = 10  # Número de elementos por página

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['now'] = timezone.now()
        return context