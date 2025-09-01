from django import forms

from .models import *

class ProductoCategoriaForm(forms.ModelForm):
    class Meta:
        model = ProductoCategoria
        fields = "__all__"
        
class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = "__all__"