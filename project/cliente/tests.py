function mostrarAlineacionTexto() {
    const contenedor = document.getElementById('alineacion-ia');
    let html = "";

    function generarHtmlEquipo(nombreEquipo, alineacion, invertidoVertical = false) {
        let htmlEquipo = `<strong>${nombreEquipo}</strong><br>`;

        // Orden táctico estándar
        let ordenPosiciones = ["Portero", "Defensa", "Medio", "Delantero"];

        // Si el equipo está invertido, se muestra de abajo hacia arriba
        if (invertidoVertical) {
            ordenPosiciones = ordenPosiciones.reverse();
        }

        ordenPosiciones.forEach(pos => {
            const jugadores = alineacion[pos];
            if (jugadores && jugadores.length > 0) {
                htmlEquipo += `
                    <div style="
                        display: flex;
                        justify-content: center;
                        margin: 6px 0;
                    ">
                `;

                jugadores.forEach(j => {
                    htmlEquipo += `
                        <div style="
                            display: flex;
                            flex-direction: column;
                            align-items: center;
                            margin: 0 10px;
                            font-weight: bold;
                            font-size: 14px;
                        ">
                            <span style="
                                display: inline-block;
                                width: 28px;
                                height: 28px;
                                line-height: 28px;
                                text-align: center;
                                border-radius: 50%;
                                background-color: ${j.color};
                                color: #fff;
                                font-weight: bold;
                                font-size: 13px;
                                box-shadow: 0 0 2px rgba(0,0,0,0.4);
                            ">
                                ${j.numero}
                            </span>
                        </div>
                    `;
                });

                htmlEquipo += `</div>`;
            }
        });

        return htmlEquipo;
    }

    // Equipo rojo: parte superior (normal)
    html += generarHtmlEquipo("Equipo Rojo", alineacionRoja, false);
    html += `<br><hr style="border:1px solid #ccc;width:60%;margin:auto;"><br>`;
    // Equipo azul: parte inferior (invertido verticalmente)
    html += generarHtmlEquipo("Equipo Azul", alineacionAzul, true);

    contenedor.innerHTML = html;
}
