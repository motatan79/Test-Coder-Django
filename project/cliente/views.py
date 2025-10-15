from django.shortcuts import render, redirect
from .forms import SeleccionJugadoresForm, ClienteForm
from . import models
import random

def index(request):
    return render(request, 'cliente/index.html')

def cliente_list(request):
    clientes = models.Cliente.objects.all()
    alineacion = None
    jugadores_seleccionados = []

    if request.method == "POST":
        if "jugadores_seleccionados" in request.POST:
            # Armar equipos
            ids = request.POST.getlist("jugadores_seleccionados")
            jugadores_seleccionados = models.Cliente.objects.filter(id__in=ids)

            jugadores_posiciones = [
                (f"{j.nombre} {j.apellido}", j.posicion1, j.posicion2)
                for j in jugadores_seleccionados
            ]

            equipoA, equipoB = armar_equipos(jugadores_posiciones)
            alineacion = formatear_equipo(equipoA, "Equipo Rojo") + "\n" + formatear_equipo(equipoB, "Equipo Azul")

            # Mantener el formulario para agregar nuevos jugadores
            form = ClienteForm()
        else:
            # Agregar nuevo jugador
            form = ClienteForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect("cliente:cliente_list")
    else:
        form = ClienteForm()

    return render(request, "cliente/cliente_list.html", {
        "clientes": clientes,
        "form": form,
        "alineacion": alineacion,
        "jugadores_seleccionados": jugadores_seleccionados,
    })
# def cliente_list(request):
#     if request.method == "POST":
#         form = ClienteForm(request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect("cliente:cliente_list")
#     else:
#         form = ClienteForm()

#     clientes = models.Cliente.objects.all()
#     return render(request, "cliente/cliente_list.html", {
#         "clientes": clientes,
#         "form": form   # 👈 aquí mandamos el form
#     })

# def cliente_list(request):
#     if request.method == "POST":
#         # Si el formulario viene en POST, creamos el cliente
#         nombre = request.POST.get("nombre")
#         apellido = request.POST.get("apellido")
#         posicion1 = request.POST.get("posicion1")
#         posicion2 = request.POST.get("posicion2")

#         if nombre and apellido and posicion1:
#             models.Cliente.objects.create(
#                 nombre=nombre,
#                 apellido=apellido,
#                 posicion1=posicion1,
#                 posicion2=posicion2,
#             )
#         # 🔹 Redirige usando namespace correcto
#         return redirect("cliente:cliente_list")

#     clientes = models.Cliente.objects.all()
#     return render(request, "cliente/cliente_list.html", {"clientes": clientes})

# Función para armar los equipos
def armar_equipos(jugadores_posiciones):
    esquema = {"Portero": 1, "Defensa": 3, "Medio": 3, "Delantero": 1}
    equipoA, equipoB = {k: [] for k in esquema}, {k: [] for k in esquema}

    # Mezclamos los jugadores
    random.shuffle(jugadores_posiciones)

    # Lista de jugadores que todavía no fueron asignados
    no_asignados = []

    # Intento de asignar por posición
    for i, jugador in enumerate(jugadores_posiciones):
        nombre, pos1, pos2 = jugador
        asignado = False

        if i % 2 == 0:  # Equipo A
            if len(equipoA[pos1]) < esquema[pos1]:
                equipoA[pos1].append(f"{nombre} ({pos1})")
                asignado = True
            elif pos2 and len(equipoA[pos2]) < esquema[pos2]:
                equipoA[pos2].append(f"{nombre} ({pos2})")
                asignado = True
        else:  # Equipo B
            if len(equipoB[pos1]) < esquema[pos1]:
                equipoB[pos1].append(f"{nombre} ({pos1})")
                asignado = True
            elif pos2 and len(equipoB[pos2]) < esquema[pos2]:
                equipoB[pos2].append(f"{nombre} ({pos2})")
                asignado = True

        if not asignado:
            no_asignados.append(jugador)

    # Asignar los jugadores restantes sin importar posición hasta completar los equipos
    equipos = [equipoA, equipoB]
    for jugador in no_asignados:
        nombre, pos1, pos2 = jugador
        for equipo in equipos:
            total_jugadores = sum(len(v) for v in equipo.values())
            if total_jugadores < 8:
                # Buscar la primera posición disponible
                for pos in ["Portero", "Defensa", "Medio", "Delantero"]:
                    if len(equipo[pos]) < esquema[pos]:
                        equipo[pos].append(f"{nombre} ({pos})")
                        break
                break

    return equipoA, equipoB

# def armar_equipos(jugadores_posiciones):
#     esquema = {"Portero": 1, "Defensa": 3, "Medio": 3, "Delantero": 1}
#     equipoA, equipoB = {k: [] for k in esquema}, {k: [] for k in esquema}

#     random.shuffle(jugadores_posiciones)

#     def asignar(jugador, equipo):
#         nombre, pos1, pos2 = jugador
#         if len(equipo[pos1]) < esquema[pos1]:
#             equipo[pos1].append(f"{nombre} ({pos1})")
#             return True
#         if len(equipo[pos2]) < esquema[pos2]:
#             equipo[pos2].append(f"{nombre} ({pos2})")
#             return True
#         return False

#     for i, jugador in enumerate(jugadores_posiciones):
#         if i % 2 == 0:
#             asignar(jugador, equipoA)
#         else:
#             asignar(jugador, equipoB)

#     return equipoA, equipoB

# Función para generar texto limpio de alineación
def formatear_equipo(equipo, nombre_equipo):
    texto = f"{nombre_equipo}\n"
    for rol in ["Portero", "Defensa", "Medio", "Delantero"]:
        jugadores = ", ".join(equipo[rol])
        texto += f"{rol}s: {jugadores}\n"
    return texto

# Vista principal del formulario de alineación
def alineacion_form(request):
    alineacion = None

    if request.method == "POST":
        form = SeleccionJugadoresForm(request.POST)
        if form.is_valid():
            jugadores_seleccionados = form.cleaned_data["jugadores"]
            jugadores_posiciones = [
                (f"{j.nombre} {j.apellido}", j.posicion1, j.posicion2)
                for j in jugadores_seleccionados
            ]

            equipoA, equipoB = armar_equipos(jugadores_posiciones)

            # Generar texto final de alineación
            alineacion = formatear_equipo(equipoA, "Equipo Azul") + "\n" + formatear_equipo(equipoB, "Equipo Rojo")

    else:
        form = SeleccionJugadoresForm()

    return render(request, "cliente/alineacion_form.html", {
        "form": form,
        "alineacion": alineacion
    })
