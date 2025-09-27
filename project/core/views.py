from django.shortcuts import render
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm, CustomUserCreationForm

# Create your views here.
def index(request):
    context = {"index": False, "about": False, "clientes": False}
    if request.path == reverse("core:index"):
        context["index"] = True
    elif request.path == reverse("core:about"):
        context["about"] = True
    elif request.path == reverse("cliente:index"):
        context["clientes"] = True
    return render(request, 'core/index.html', context)

# def about(request: HttpRequest) -> HttpResponse: 
#     return render(request, 'core/about.html', {'nombre': 'Calcio 2.1'})

class CustomLoginView(LoginView):
    authentication_form = CustomAuthenticationForm
    template_name = 'core/login.html'
    redirect_authenticated_user = True
    
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            # Aquí podrías redirigir al usuario a la página de login o a otra página
            return render(request, 'core/index.html', {})
    else:
        form = CustomUserCreationForm()
        return render(request, 'core/register.html', {"form": form})