# Vista para formulario y resultado en HTML
def alineacion_form(request):
    alineacion = None
    if request.method == 'POST':
        jugadores = []
        posiciones = []
        for i in range(16):
            nombre = request.POST.get(f'jugador{i}')
            posicion = request.POST.get(f'posicion{i}')
            if nombre and posicion:
                jugadores.append(nombre)
                posiciones.append(posicion)

        prompt = f"Arma dos equipos de fútbol 8 con estos jugadores y posiciones: {list(zip(jugadores, posiciones))}. Devuelve la alineación para cada equipo de forma clara."
        import openai, os
        openai.api_key = os.getenv('OPENAI_API_KEY', 'TU_API_KEY_AQUI')
        try:
            response = openai.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=[{"role": "user", "content": prompt}],
                max_tokens=500,
                temperature=0.7
            )
            content = response.choices[0].message.content
            if content:
                alineacion = content.strip()
            else:
                alineacion = "No se recibió respuesta de la IA."
        except Exception as e:
            alineacion = f"Error: {str(e)}"
    return render(request, 'cliente/alineacion_form.html', {'alineacion': alineacion, 'rango': range(16)})
from django.shortcuts import render, redirect
from . import models
from . import forms

# Create your views here.
def index(request):
    return render(request, 'cliente/index.html')

def cliente_list(request):
    from .forms import ClienteForm
    from django.contrib import messages
    import openai, os
    clientes = models.Cliente.objects.all()
    form = ClienteForm()
    alineacion = None
    jugadores_seleccionados = []
    if request.method == 'POST':
        # Si el submit viene del formulario de alineación (checkboxes)
        if 'jugadores_seleccionados' in request.POST:
            ids = request.POST.getlist('jugadores_seleccionados')
            jugadores_seleccionados = list(models.Cliente.objects.filter(id__in=ids))
            # Construir prompt para IA
            jugadores_posiciones = [
                f"{j.nombre} {j.apellido} ({j.posicion1 or ''}/{j.posicion2 or ''})" for j in jugadores_seleccionados
            ]
            prompt = (
                "Eres un entrenador experto en fútbol 8. "
                "Con los siguientes jugadores y sus posiciones principales/secundarias, arma dos equipos equilibrados. "
                "Cada equipo debe tener: 1 portero, 3 defensas, 3 mediocampistas y 1 delantero. "
                "Respeta las posiciones preferidas de cada jugador y distribúyelos para maximizar el rendimiento. "
                "No repitas jugadores en la misma posición. "
                "Si todas las posiciones principales (posición1) ya están ocupadas, asigna al jugador en su posición secundaria (posición2). "
                "Devuelve la alineación de cada equipo en formato claro, indicando nombre y posición, y lista para visualizar en una cancha." 
                f" Jugadores: {jugadores_posiciones}."
            )
            openai.api_key = os.getenv('OPENAI_API_KEY', 'TU_API_KEY_AQUI')
            try:
                response = openai.chat.completions.create(
                    model="gpt-3.5-turbo",
                    messages=[{"role": "user", "content": prompt}],
                    max_tokens=500,
                    temperature=0.7
                )
                content = response.choices[0].message.content
                if content:
                    alineacion = content.strip()
                else:
                    alineacion = "No se recibió respuesta de la IA."
            except Exception as e:
                alineacion = f"Error: {str(e)}"
        else:
            # Formulario de agregar jugador
            form = ClienteForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request, '¡Jugador agregado exitosamente!')
                return redirect('cliente:cliente_list')
    context = {
        'clientes': clientes,
        'form': form,
        'jugadores_seleccionados': jugadores_seleccionados,
        'alineacion': alineacion,
    }
    return render(request, 'cliente/cliente_list.html', context)

def cliente_create(request):
    if request.method == 'POST':
        form = forms.ClienteForm(request.POST)
        if form.is_valid():
            cliente = form.save()
            return redirect('cliente:cliente_list')
    else: # request.method == 'GET':
        form = forms.ClienteForm()
    return render(request, 'cliente/cliente_create.html', {'form': form})
    