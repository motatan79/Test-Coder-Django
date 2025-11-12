from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest
from django.urls import reverse
from django.contrib.auth.views import LoginView
from .forms import CustomAuthenticationForm, CustomUserCreationForm
from django.contrib.sites.shortcuts import get_current_site
from django.template.loader import render_to_string
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.contrib.auth.tokens import default_token_generator
from django.core.mail import send_mail
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.models import User
from .forms import CustomUserCreationForm
from django.conf import settings
from django.contrib.auth.views import PasswordResetView
from django.core.mail import EmailMultiAlternatives
from django.urls import reverse_lazy

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
    
# def register(request):
#     if request.method == 'POST':
#         form = CustomUserCreationForm(request.POST)
#         if form.is_valid():
#             form.save()
#             # Redirigimos al índice (o podrías cambiar a la página de login)
#             return redirect('core:index')
#         else:
#             # Si el formulario no es válido, renderizar la página de registro con errores
#             return render(request, 'core/register.html', {"form": form})
#     else:
#         form = CustomUserCreationForm()
#         return render(request, 'core/register.html', {"form": form})

class CustomPasswordResetView(PasswordResetView):
    template_name = "core/password_reset.html"
    email_template_name = "core/password_reset_email.html"
    html_email_template_name = "core/password_reset_email.html"
    subject_template_name = "core/password_reset_subject.txt"
    success_url = reverse_lazy("core:password_reset_done")

    def send_mail(self, subject_template_name, email_template_name, context,
                  from_email, to_email, html_email_template_name=None):
        """
        Enviamos un ÚNICO correo HTML, evitando el doble envío de Django.
        """
        subject = render_to_string(subject_template_name, context).strip()
        html_content = render_to_string(self.html_email_template_name, context)

        msg = EmailMultiAlternatives(
            subject=subject,
            body="Para ver este mensaje, abrilo en un cliente compatible con HTML.",
            from_email=from_email,
            to=[to_email],
        )
        msg.attach_alternative(html_content, "text/html")
        msg.send(fail_silently=False)

    # ⚠️ Este método anula el envío duplicado
    def send_email(self, *args, **kwargs):
        pass

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = False  # 🚫 El usuario no puede iniciar sesión aún
            user.save()

            # Crear token y enlace
            current_site = get_current_site(request)
            subject = 'Activa tu cuenta'
            message = render_to_string('core/activation_email.html', {
                'user': user,
                'domain': current_site.domain,
                'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                'token': default_token_generator.make_token(user),
            })

            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, [user.email])
            messages.info(request, 'Te hemos enviado un correo para activar tu cuenta. Revisa tu bandeja de entrada.')
            return redirect('core:login')
    else:
        form = CustomUserCreationForm()
    
    return render(request, 'core/register.html', {'form': form})

# 🔹 Vista que recibe el clic del email
def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, 'Tu cuenta ha sido activada correctamente. Ya puedes iniciar sesión.')
        return redirect('core:login')
    else:
        messages.error(request, 'El enlace de activación no es válido o ha expirado.')
        return redirect('core:register')
