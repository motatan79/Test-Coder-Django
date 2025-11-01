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
    # Obtener jugadores visibles para el usuario
    perfil = getattr(request.user, "perfil", None)
    if perfil and perfil.equipo:
        jugadores = models.Cliente.objects.filter(equipo=perfil.equipo)
    else:
        jugadores = models.Cliente.objects.all() if (request.user.is_staff or request.user.is_superuser) else models.Cliente.objects.none()

    clientes = jugadores
    alineacion = None
    jugadores_seleccionados = []

    # Formaciones: cada valor es la cantidad POR EQUIPO
    FORMACIONES = {
        5: {"Portero": 1, "Defensa": 2, "Medio": 1, "Delantero": 1},
        8: {"Portero": 1, "Defensa": 3, "Medio": 3, "Delantero": 1},
        11: {"Portero": 1, "Defensa": 4, "Medio": 3, "Delantero": 3},
    }

    # Manejo de creación de jugador (botón "Agregar jugador" debe enviar name="agregar_jugador")
    if request.method == "POST" and "agregar_jugador" in request.POST:
        form = ClienteForm(request.POST)
        if form.is_valid():
            nuevo = form.save(commit=False)
            perfil = getattr(request.user, "perfil", None)
            if perfil and perfil.equipo:
                nuevo.equipo = perfil.equipo
            else:
                nuevo.equipo = models.Equipo.objects.first()
            nuevo.save()
            messages.success(request, f"Jugador {nuevo.nombre} {nuevo.apellido} agregado correctamente.")
            return redirect("cliente:cliente_list")
        # si no es válido, seguimos para render con errores
        else: 
            messages.error(request, "La posición secundaria debe ser diferente a la principal")

    # Lógica de crear alineación — el selector envía "tipo-partido" y los checkboxes name="jugadores_seleccionados"
    if request.method == "POST" and "jugadores_seleccionados" in request.POST:
        ids = request.POST.getlist("jugadores_seleccionados")
        jugadores_seleccionados = list(models.Cliente.objects.filter(id__in=ids))

        # tipo de partido (5,8,11)
        try:
            tipo_partido = int(request.POST.get("tipo-partido", 8))
        except (ValueError, TypeError):
            tipo_partido = 8

        distribucion = FORMACIONES.get(tipo_partido, FORMACIONES[8])

        # Agrupar jugadores por posición principal
        por_posicion = {"Portero": [], "Defensa": [], "Medio": [], "Delantero": []}
        for j in jugadores_seleccionados:
            pos = j.posicion1 if j.posicion1 in por_posicion else "Medio"
            por_posicion[pos].append(j)

        # Mezclar cada lista para aleatoriedad
        for lista in por_posicion.values():
            random.shuffle(lista)

        equipoA, equipoB = [], []
        usados_ids = set()

        # Para cada posición tomamos hasta `cantidad_por_equipo` para A y luego para B.
        for posicion, cantidad_por_equipo in distribucion.items():
            jugadores_pos = [j for j in por_posicion[posicion] if j.id not in usados_ids]

            # asignados para A y B (si hay suficientes)
            asignadosA = jugadores_pos[:cantidad_por_equipo]
            asignadosB = jugadores_pos[cantidad_por_equipo:cantidad_por_equipo*2]

            equipoA += [(j, posicion) for j in asignadosA]
            equipoB += [(j, posicion) for j in asignadosB]
            usados_ids.update(j.id for j in asignadosA + asignadosB)

        # Jugadores aún no usados — pool para rellenar faltantes
        no_asignados = [j for j in jugadores_seleccionados if j.id not in usados_ids]
        random.shuffle(no_asignados)

        # Función que rellena las posiciones faltantes de UN equipo
        def rellenar(equipo):
            # conteo actual por posición en ese equipo
            conteo = {pos: 0 for pos in distribucion}
            for j, pos_asignada in equipo:
                if pos_asignada in conteo:
                    conteo[pos_asignada] += 1
            # crear lista de faltantes (por posición) según distribucion POR EQUIPO
            faltantes = []
            for pos, req in distribucion.items():
                faltantes.extend([pos] * max(0, req - conteo.get(pos, 0)))
            # asignar desde no_asignados
            while faltantes and no_asignados:
                pos = faltantes.pop(0)
                j = no_asignados.pop(0)
                equipo.append((j, pos))
                usados_ids.add(j.id)

        # rellenar ambos equipos
        rellenar(equipoA)
        rellenar(equipoB)

        # Si todavía faltan (escasez total de jugadores), tratar de completar con cualquier jugador restante (si existiera)
        # — en ese caso equipos pueden quedar incompletos si realmente faltan jugadores.
        # Generar texto final con la posición asignada
        alineacion = formatear_equipo(
            [(f"{j.nombre} {j.apellido}", pos, j.posicion2) for j, pos in equipoA]
        )
        alineacion += "\n" + formatear_equipo(
            [(f"{j.nombre} {j.apellido}", pos, j.posicion2) for j, pos in equipoB]
        )
        
        # 🔹 Extraer nombres para mostrar en cancha
        equipoA_jugadores = [f"{j.nombre} {j.apellido}" for j, pos in equipoA]
        equipoB_jugadores = [f"{j.nombre} {j.apellido}" for j, pos in equipoB]        

        form = ClienteForm()
    else:
        form = ClienteForm()
        tipo_partido = 8  # valor por defecto para el template
        equipoA_jugadores = []
        equipoB_jugadores = []


    equipo_usuario = models.Equipo.objects.filter(creador=request.user).first() if request.user.is_authenticated else None

    # pasar tambien tipo_partido al template para mostrar el cartel "N vs N"
    return render(request, "cliente/cliente_list.html", {
        "clientes": clientes,
        "form": form,
        "alineacion": alineacion,
        "jugadores_seleccionados": jugadores_seleccionados,
        "equipo": equipo_usuario,
        "tipo_partido": tipo_partido,
        "equipoA_jugadores": equipoA_jugadores,
        "equipoB_jugadores": equipoB_jugadores,
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

def formatear_equipo(equipo, nombre_equipo=None):
    posiciones = {"Portero": [], "Defensa": [], "Medio": [], "Delantero": []}

    for jugador in equipo:
        nombre, pos1, pos2 = jugador
        if pos1 in posiciones:
            posiciones[pos1].append(f"{nombre}")
        else:
            posiciones["Medio"].append(f"{nombre}")

    resultado = []
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
            alineacion = formatear_equipo(equipoA) + "\n" + formatear_equipo(equipoB)

    else:
        form = SeleccionJugadoresForm()

    return render(request, "cliente/alineacion_form.html", {
        "form": form,
        "alineacion": alineacion
    })
