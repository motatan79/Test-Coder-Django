@login_required
def cliente_list(request):
    perfil = getattr(request.user, 'perfil', None)
    if perfil and perfil.equipo:
        jugadores = models.Cliente.objects.filter(equipo=perfil.equipo)
    else:
        jugadores = models.Cliente.objects.all() if request.user.is_staff or request.user.is_superuser else models.Cliente.objects.none()

    clientes = jugadores
    alineacion = None
    jugadores_seleccionados = []

    # Definir formaciones por tipo de partido
    FORMACIONES = {
        5: {"Portero": 1, "Defensa": 2, "Medio": 1, "Delantero": 1},
        8: {"Portero": 1, "Defensa": 3, "Medio": 3, "Delantero": 1},
        11: {"Portero": 1, "Defensa": 4, "Medio": 3, "Delantero": 3},
    }

    if request.method == "POST":
        if "agregar_jugador" in request.POST:
            # Formulario de agregar jugador
            form = ClienteForm(request.POST)
            if form.is_valid():
                nuevo = form.save(commit=False)
                perfil = getattr(request.user, 'perfil', None)
                if perfil and perfil.equipo:
                    nuevo.equipo = perfil.equipo
                else:
                    # Asignar primer equipo disponible si no hay perfil/equipo
                    equipo_default = models.Equipo.objects.first()
                    nuevo.equipo = equipo_default
                nuevo.save()
                messages.success(request, f"Jugador {nuevo.nombre} {nuevo.apellido} agregado correctamente.")
                return redirect("cliente:cliente_list")
            else:
                # Mantener errores si hay
                pass
        elif "jugadores_seleccionados" in request.POST:
            # Lógica de selección y alineación
            ids = request.POST.getlist("jugadores_seleccionados")
            jugadores_seleccionados = list(models.Cliente.objects.filter(id__in=ids))
 
    
    if request.method == "POST" and "jugadores_seleccionados" in request.POST:
        ids = request.POST.getlist("jugadores_seleccionados")
        jugadores_seleccionados = list(models.Cliente.objects.filter(id__in=ids))

        tipo_partido = int(request.POST.get("tipo-partido", 8))
        distribucion = FORMACIONES.get(tipo_partido, FORMACIONES[8])

        # Agrupar jugadores por posición principal
        por_posicion = {"Portero": [], "Defensa": [], "Medio": [], "Delantero": []}
        for j in jugadores_seleccionados:
            pos = j.posicion1 if j.posicion1 in por_posicion else "Medio"
            por_posicion[pos].append(j)

        # Mezclar jugadores por posición
        for lista in por_posicion.values():
            random.shuffle(lista)

        equipoA, equipoB = [], []
        usados_ids = set()

        # Asignar jugadores por posición, balanceando entre A y B
        for posicion, cantidad_total in distribucion.items():
            cantidadA = cantidad_total // 2
            cantidadB = cantidad_total - cantidadA
            jugadores_pos = [j for j in por_posicion[posicion] if j.id not in usados_ids]

            asignadosA = jugadores_pos[:cantidadA]
            asignadosB = jugadores_pos[cantidadA:cantidadA+cantidadB]

            equipoA += [(j, posicion) for j in asignadosA]
            equipoB += [(j, posicion) for j in asignadosB]

            usados_ids.update(j.id for j in asignadosA + asignadosB)

        # Rellenar posiciones faltantes con jugadores no asignados
        no_asignados = [j for j in jugadores_seleccionados if j.id not in usados_ids]
        random.shuffle(no_asignados)

        def rellenar(equipo):
            conteo = {pos: 0 for pos in distribucion}
            for j, pos_asignada in equipo:
                conteo[pos_asignada] += 1
            faltantes = []
            for pos, req in distribucion.items():
                faltantes.extend([pos] * (req - conteo[pos]))
            while faltantes and no_asignados:
                pos = faltantes.pop(0)
                j = no_asignados.pop(0)
                equipo.append((j, pos))
                usados_ids.add(j.id)

        rellenar(equipoA)
        rellenar(equipoB)

        # Generar alineación final
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
        form = ClienteForm()

    equipo_usuario = models.Equipo.objects.filter(creador=request.user).first() if request.user.is_authenticated else None

    return render(request, "cliente/cliente_list.html", {
        "clientes": clientes,
        "form": form,
        "alineacion": alineacion,
        "jugadores_seleccionados": jugadores_seleccionados,
        "equipo": equipo_usuario,
    })


<style>
    .jugador {
    position: absolute;
    background: rgba(0, 102, 204, 0.9); /* azul */
    color: white;
    padding: 4px 6px;
    border-radius: 6px;
    font-size: 12px;
    text-align: center;
    transform: translate(-50%, -50%);
    white-space: nowrap;
    }
    .btn-main {
        background: #3498db;
        color: #fff;
        border: none;
        padding: 10px 16px;
        border-radius: 6px;
        cursor: pointer;
        transition: background 0.3s;
    }

    .btn-main:disabled {
        background: #aaa;
        cursor: not-allowed;
    }

    .btn-main:hover:enabled {
        background: #2980b9;
    }

    input,
    select {
        width: 100%;
        padding: 6px;
        border: 1px solid #ccc;
        border-radius: 4px;
    }

    .cancha-container {
        display: flex;
        justify-content: center;
        align-items: center;
        margin: 32px 0;
    }

    .cancha {
        position: relative;
        width: 90vw;
        max-width: 600px;
        height: 60vw;
        max-height: 400px;
        background: #228B22;
        border: 4px solid #fff;
        border-radius: 24px;
        box-shadow: 0 2px 16px rgba(0, 0, 0, 0.12);
    }

    .linea-centro {
        position: absolute;
        left: 50%;
        top: 0;
        width: 4px;
        height: 100%;
        background: #fff;
        transform: translateX(-50%);
    }

    .circulo-centro {
        position: absolute;
        left: 50%;
        top: 50%;
        width: 80px;
        height: 80px;
        border: 3px solid #fff;
        border-radius: 50%;
        transform: translate(-50%, -50%);
    }

    .area {
        position: absolute;
        width: 80px;
        height: 180px;
        border: 3px solid #fff;
        border-radius: 16px;
        top: 50%;
        transform: translateY(-50%);
    }

    .area-izq {
        left: 0;
    }

    .area-der {
        right: 0;
    }
</style>

<script>
document.addEventListener('DOMContentLoaded', function () {
    const tipoSelect = document.getElementById('tipo-partido');
    const tipoHidden = document.getElementById('tipo-partido-hidden');
    const checkboxes = () => Array.from(document.querySelectorAll('.jugador-checkbox'));
    const listaSeleccionados = document.getElementById('jugadores-seleccionados-list');
    const btnAlineacion = document.getElementById('crear-alineacion-btn');
    const numSeleccionados = document.getElementById('num-seleccionados');
    const totalNecesarios = document.getElementById('total-necesarios');
    const bloqueIzquierdo = document.getElementById('bloque-izquierdo');

    const FORMACIONES_TOTALES = {5: 10, 8: 16, 11: 22};

    function actualizarUI() {
        const boxes = checkboxes();
        let seleccionados = boxes.filter(cb => cb.checked).length;
        listaSeleccionados.innerHTML = '';

        boxes.filter(cb => cb.checked).forEach(cb => {
            const fila = cb.closest('tr');
            if (!fila) return;
            const nombre = fila.children[1]?.innerText || '';
            const apellido = fila.children[2]?.innerText || '';
            const li = document.createElement('li');
            li.textContent = (nombre + ' ' + apellido).trim();
            listaSeleccionados.appendChild(li);
        });

        const tipo = parseInt(tipoSelect.value) || 8;
        const necesarios = FORMACIONES_TOTALES[tipo] || (tipo * 2);
        totalNecesarios.textContent = necesarios;
        numSeleccionados.textContent = seleccionados;
        btnAlineacion.disabled = (seleccionados !== necesarios);
        tipoHidden.value = tipo;

        const alturaBase = 568;
        const extra = Math.max(0, listaSeleccionados.scrollHeight - 80);
        if (bloqueIzquierdo) bloqueIzquierdo.style.height = (alturaBase + extra) + 'px';
    }

    tipoSelect.addEventListener('change', actualizarUI);
    checkboxes().forEach(cb => cb.addEventListener('change', actualizarUI));
    actualizarUI();

    // 🔹 función para mostrar jugadores en cancha
    function mostrarJugadoresEnCancha() {
        const equipoRojo = document.getElementById('equipo-rojo');
        const equipoAzul = document.getElementById('equipo-azul');
        equipoRojo.innerHTML = '';
        equipoAzul.innerHTML = '';

        // posiciones ejemplo 5vs5
        const posiciones = {
            rojo: [
                { top: '70%', left: '80%', nombre: 'Portero Rojo' },
                { top: '50%', left: '65%', nombre: 'Defensa 1' },
                { top: '30%', left: '65%', nombre: 'Defensa 2' },
                { top: '45%', left: '45%', nombre: 'Medio' },
                { top: '50%', left: '25%', nombre: 'Delantero' }
            ],
            azul: [
                { top: '30%', left: '20%', nombre: 'Portero Azul' },
                { top: '45%', left: '35%', nombre: 'Defensa 1' },
                { top: '55%', left: '35%', nombre: 'Defensa 2' },
                { top: '45%', left: '55%', nombre: 'Medio' },
                { top: '50%', left: '75%', nombre: 'Delantero' }
            ]
        };

        posiciones.rojo.forEach((pos, i) => {
            const j = document.createElement('div');
            j.className = 'jugador rojo';
            j.textContent = i + 1;
            j.style.top = pos.top;
            j.style.left = pos.left;
            j.dataset.nombre = pos.nombre;
            equipoRojo.appendChild(j);
        });

        posiciones.azul.forEach((pos, i) => {
            const j = document.createElement('div');
            j.className = 'jugador azul';
            j.textContent = i + 1;
            j.style.top = pos.top;
            j.style.left = pos.left;
            j.dataset.nombre = pos.nombre;
            equipoAzul.appendChild(j);
        });
    }

    // 🔹 al crear alineación, mostramos los jugadores
    btnAlineacion.addEventListener('click', (e) => {
        e.preventDefault();
        mostrarJugadoresEnCancha();
    });
});
</script>

