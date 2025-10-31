<script>
document.addEventListener("DOMContentLoaded", function () {
  const formaciones = {
    5: { Portero: 1, Defensa: 2, Medio: 1, Delantero: 1 },
    8: { Portero: 1, Defensa: 3, Medio: 3, Delantero: 1 },
    11:{ Portero: 1, Defensa: 4, Medio: 3, Delantero: 3 },
  };

  const tipo = parseInt("{{ tipo_partido|default:5 }}") || 5;
  const formacion = formaciones[tipo];

  const equipoRojo = document.getElementById("equipo-rojo");
  const equipoAzul = document.getElementById("equipo-azul");
  equipoRojo.innerHTML = "";
  equipoAzul.innerHTML = "";

  // ========================
  // 📍 Posiciones verticales
  // ========================
  const posiciones = {
    5: {
      Portero:  { y: [50] },
      Defensa:  { y: [40, 60] },
      Medio:    { y: [50] },
      Delantero:{ y: [50] }
    },
    8: {
      Portero:  { y: [50] },
      Defensa:  { y: [35, 50, 65] },
      Medio:    { y: [35, 50, 65] },
      Delantero:{ y: [50] }
    },
    11: {
      Portero:  { y: [50] },
      Defensa:  { y: [30, 45, 60, 75] },
      Medio:    { y: [30, 50, 70] },
      Delantero:{ y: [25, 50, 75] }
    }
  };

  // ========================
  // ⚽ Crear jugador como círculo con número
  // ========================
  function crearJugador(x, y, color, numero) {
    const jugador = document.createElement("div");
    jugador.className = "jugador";
    jugador.style.position = "absolute";
    jugador.style.left = x + "%";
    jugador.style.top = y + "%";
    jugador.style.transform = "translate(-50%, -50%)";
    jugador.style.width = "30px";
    jugador.style.height = "30px";
    jugador.style.borderRadius = "50%";
    jugador.style.backgroundColor = color;
    jugador.style.border = "2px solid #fff";
    jugador.style.display = "flex";
    jugador.style.alignItems = "center";
    jugador.style.justifyContent = "center";
    jugador.style.color = "#fff";
    jugador.style.fontWeight = "bold";
    jugador.textContent = numero;
    return jugador;
  }

  // ========================
  // 🟥 Equipo ROJO (izquierda)
  // ========================
  const offsetXRojo = {
    5: [10, 25, 30, 40],
    8: [10, 25, 40, 47],
    11:[8, 18, 28, 40]
  }[tipo];

  let idx = 0;
  let numJugador = 1;
  for (let pos in formacion) {
    const cant = formacion[pos];
    const yVals = posiciones[tipo][pos].y.slice(0, cant);
    yVals.forEach((y) => {
      const jugador = crearJugador(offsetXRojo[idx], y, "#e74c3c", numJugador);
      equipoRojo.appendChild(jugador);
      numJugador++;
    });
    idx++;
  }

  // ========================
  // 🟦 Equipo AZUL (derecha)
  // ========================
  const offsetXAzul = {
    5: [90, 75, 70, 60],
    8: [90, 75, 60, 53],
    11:[92, 82, 72, 60]
  }[tipo];

  idx = 0;
  numJugador = 1;
  for (let pos in formacion) {
    const cant = formacion[pos];
    const yVals = posiciones[tipo][pos].y.slice(0, cant);
    yVals.forEach((y) => {
      const jugador = crearJugador(offsetXAzul[idx], y, "#3498db", numJugador);
      equipoAzul.appendChild(jugador);
      numJugador++;
    });
    idx++;
  }
});
</script>