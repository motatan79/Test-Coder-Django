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
            # Obtener jugadores seleccionados
            ids = request.POST.getlist("jugadores_seleccionados")
            jugadores_seleccionados = list(models.Cliente.objects.filter(id__in=ids))

            # Tipo de partido (5, 8 o 11)
            tipo_partido = int(request.POST.get("tipo-partido", 8))

            # Formaciones por tipo de partido
            formaciones = {
                5: {"Portero": 1, "Defensa": 2, "Medio": 1, "Delantero": 1},
                8: {"Portero": 1, "Defensa": 3, "Medio": 3, "Delantero": 1},
                11: {"Portero": 1, "Defensa": 4, "Medio": 3, "Delantero": 3},
            }
            distribucion = formaciones.get(tipo_partido, formaciones[8])
            total_por_equipo = sum(distribucion.values())

            # Agrupar por posición principal
            por_posicion = {"Portero": [], "Defensa": [], "Medio": [], "Delantero": []}
            for j in jugadores_seleccionados:
                pos = j.posicion1 if j.posicion1 in por_posicion else "Medio"
                por_posicion[pos].append(j)

            # Mezclar cada lista de posición
            for lista in por_posicion.values():
                random.shuffle(lista)


            # Equipos vacíos (listas de tuplas: (jugador, posicion_asignada))
            equipoA, equipoB = [], []
            usados_ids = set()

            # Intentar asignar posiciones según la formación
            for posicion, cantidad in distribucion.items():
                # Cuántos necesita cada equipo
                necesarios = cantidad

                # Tomar los jugadores disponibles para esa posición
                jugadores_pos = [j for j in por_posicion[posicion] if j.id not in usados_ids]

                # Equipo A
                asignadosA = jugadores_pos[:necesarios]
                equipoA += [(j, posicion) for j in asignadosA]
                usados_ids.update(j.id for j in asignadosA)

                # Equipo B
                asignadosB = jugadores_pos[necesarios:necesarios*2]
                equipoB += [(j, posicion) for j in asignadosB]
                usados_ids.update(j.id for j in asignadosB)

            # Obtener los que quedan sin asignar
            no_asignados = [j for j in jugadores_seleccionados if j.id not in usados_ids]
            random.shuffle(no_asignados)

            # Rellenar posiciones vacías con cualquier jugador disponible
            def rellenar(equipo, nombre_equipo):
                faltantes = []
                conteo = {pos:0 for pos in distribucion}
                for j, pos_asignada in equipo:
                    conteo[pos_asignada] += 1
                for pos, req in distribucion.items():
                    if conteo[pos] < req:
                        for _ in range(req - conteo[pos]):
                            faltantes.append(pos)
                # Asignar faltantes
                while faltantes and no_asignados:
                    pos = faltantes.pop(0)
                    j = no_asignados.pop(0)
                    equipo.append((j, pos))
                    usados_ids.add(j.id)
                # Si aún faltan, tomar de todos los seleccionados (aunque repita)
                todos = [j for j in jugadores_seleccionados if j.id not in usados_ids]
                random.shuffle(todos)
                while faltantes and todos:
                    pos = faltantes.pop(0)
                    j = todos.pop(0)
                    equipo.append((j, pos))
                    usados_ids.add(j.id)

            rellenar(equipoA, "Equipo Rojo")
            rellenar(equipoB, "Equipo Azul")

            # Formatear resultado final
            alineacion = formatear_equipo(
                [(f"{j.nombre} {j.apellido}", pos, j.posicion2) for j, pos in equipoA],
                "Equipo Rojo"
            )
            alineacion += "\n" + formatear_equipo(
                [(f"{j.nombre} {j.apellido}", pos, j.posicion2) for j, pos in equipoB],
                "Equipo Azul"
            )


            # Formatear resultado final usando la posición asignada
            alineacion = formatear_equipo(
                [(f"{j.nombre} {j.apellido}", pos, j.posicion2) for j, pos in equipoA],
                "Equipo Rojo"
            )
            alineacion += "\n" + formatear_equipo(
                [(f"{j.nombre} {j.apellido}", pos, j.posicion2) for j, pos in equipoB],
                "Equipo Azul"
            )

            form = ClienteForm()

        else:
            # Caso: agregar nuevo jugador
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
def armar_equipos(jugadores_posiciones, tipo_partido=5):
    # Formaciones según tipo de partido
    formaciones = {
        5: {"Portero": 1, "Defensa": 2, "Medio": 1, "Delantero": 1},
        8: {"Portero": 1, "Defensa": 3, "Medio": 3, "Delantero": 1},
        11: {"Portero": 1, "Defensa": 4, "Medio": 3, "Delantero": 3},
    }
    esquema = formaciones.get(tipo_partido, formaciones[8])

    equipoA, equipoB = {k: [] for k in esquema}, {k: [] for k in esquema}

    # Mezclar los jugadores
    random.shuffle(jugadores_posiciones)

    # Lista de jugadores no asignados
    no_asignados = []

    # Asignar jugadores respetando la formación
    for i, jugador in enumerate(jugadores_posiciones):
        nombre, pos1, pos2 = jugador
        asignado = False

        # Determinar equipo
        equipo = equipoA if i % 2 == 0 else equipoB

        # Intentar posición principal
        if len(equipo[pos1]) < esquema[pos1]:
            equipo[pos1].append(f"{nombre} ({pos1})")
            asignado = True
        # Intentar posición secundaria
        elif pos2 and len(equipo[pos2]) < esquema[pos2]:
            equipo[pos2].append(f"{nombre} ({pos2})")
            asignado = True

        if not asignado:
            no_asignados.append(jugador)

    # Rellenar posiciones vacías con jugadores no asignados
    for equipo in [equipoA, equipoB]:
        for pos, limite in esquema.items():
            while len(equipo[pos]) < limite and no_asignados:
                j = no_asignados.pop(0)
                nombre, pos1, pos2 = j
                equipo[pos].append(f"{nombre} ({pos})")

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
    posiciones = {"Portero": [], "Defensa": [], "Medio": [], "Delantero": []}

    for jugador in equipo:
        nombre, pos1, pos2 = jugador
        if pos1 in posiciones:
            posiciones[pos1].append(f"{nombre}")
        else:
            posiciones["Medio"].append(f"{nombre}")

    resultado = [f"\n{nombre_equipo}"]
    for pos, jugadores in posiciones.items():
        resultado.append(f"{pos}s: {', '.join(jugadores) if jugadores else '-'}")
    return "\n".join(resultado)

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
