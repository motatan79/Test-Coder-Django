from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .forms import SeleccionJugadoresForm, ClienteForm, EquipoForm, PerfilForm
from . import models
import random
from .forms import EquipoForm, PerfilForm
from django.contrib import messages
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm


def index(request):
    return render(request, 'cliente/index.html')

@login_required
def cliente_list(request):
    # Determinar equipo del usuario a través de su perfil
    perfil = getattr(request.user, 'perfil', None)
    if perfil and perfil.equipo:
        jugadores = models.Cliente.objects.filter(equipo=perfil.equipo)
    else:
        # si es staff, mostrar todos; si no, ninguno
        if request.user.is_staff or request.user.is_superuser:
            jugadores = models.Cliente.objects.all()
        else:
            jugadores = models.Cliente.objects.none()

    clientes = jugadores
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
                nuevo = form.save(commit=False)
                perfil = getattr(request.user, 'perfil', None)
                if perfil and perfil.equipo:
                    nuevo.equipo = perfil.equipo
                else:
                    # Si el usuario no tiene perfil/equipo, asignar un equipo por defecto si existe
                    try:
                        nuevo.equipo = models.Equipo.objects.first()
                    except Exception:
                        nuevo.equipo = None
                # nuevo.equipo debe existir (FK no nula); si no existe, form validation debería haber evitado esto
                nuevo.save()
                return redirect("cliente:cliente_list")
            else:
                # Si el formulario no es válido, dejamos que al final se renderice con los errores
                pass

    else:
        form = ClienteForm()

    # return render(request, "cliente/cliente_list.html", {
    #     "clientes": clientes,
    #     "form": form,
    #     "alineacion": alineacion,
    #     "jugadores_seleccionados": jugadores_seleccionados,
    # })
    # Obtener el equipo del usuario autenticado (si existe)
    equipo_usuario = None
    if request.user.is_authenticated:
        equipo_usuario = models.Equipo.objects.filter(creador=request.user).first()

    return render(request, "cliente/cliente_list.html", {
        "clientes": clientes,
        "form": form,
        "alineacion": alineacion,
        "jugadores_seleccionados": jugadores_seleccionados,
        "equipo": equipo_usuario,  # 👉 pasamos el equipo al template
    })



@login_required
def mi_equipo(request):
    perfil = getattr(request.user, 'perfil', None)
    equipo = perfil.equipo if perfil else None
    return render(request, 'cliente/mi_equipo.html', {'equipo': equipo})


def crear_equipo(request, equipo_id=None):
    equipos = models.Equipo.objects.all().order_by('nombre')

    # Si el usuario NO está autenticado → mostrar login/register
    if not request.user.is_authenticated:
        login_form = AuthenticationForm()
        register_form = UserCreationForm()

        if request.method == 'POST' and 'login' in request.POST:
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                user = login_form.get_user()
                login(request, user)
                return redirect('cliente:crear_equipo')

        elif request.method == 'POST' and 'register' in request.POST:
            register_form = UserCreationForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                return redirect('cliente:crear_equipo')

        return render(request, 'cliente/crear_equipo.html', {
            'equipos': equipos,
            'login_form': login_form,
            'register_form': register_form,
        })

    # Usuario autenticado: crear o editar equipo
    perfil = getattr(request.user, 'perfil', None)

    equipo_edit = None
    if equipo_id:
        equipo_edit = get_object_or_404(models.Equipo, id=equipo_id)
        # Solo permitir editar si el equipo fue creado por este usuario
        if equipo_edit.creador != request.user:
            messages.error(request, "No tienes permiso para editar este equipo.")
            return redirect('cliente:crear_equipo')

    if request.method == 'POST':
        form = EquipoForm(request.POST, instance=equipo_edit)
        if form.is_valid():
            equipo = form.save(commit=False)
            equipo.creador = request.user
            equipo.save()

            if perfil:
                perfil.equipo = equipo
                perfil.save()

            if equipo_edit:
                messages.success(request, 'Equipo actualizado correctamente.')
            else:
                messages.success(request, 'Equipo creado y asignado a tu perfil.')

            return redirect('cliente:crear_equipo')
    else:
        form = EquipoForm(instance=equipo_edit)

    return render(request, 'cliente/crear_equipo.html', {
        'equipos': equipos,
        'form': form,
        'equipo_edit': equipo_edit,
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
