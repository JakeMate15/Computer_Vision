// script.js

document.addEventListener('DOMContentLoaded', function() {
    // Elementos del DOM
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const btnCargar = document.getElementById('btnCargar');
    const btnGuardar = document.getElementById('btnGuardar');
    const btnAnalizar = document.getElementById('btnAnalizar');
    const selectorImagen = document.getElementById('selectorImagen');
    const selectorCriterio = document.getElementById('selectorCriterio');
    const listaClases = document.getElementById('listaClases');
    const contenedorResultados = document.getElementById('contenedorResultados');

    let imagen = new Image();
    let seleccion = {};
    let seleccionando = false;
    let imagenCargada = false;

    function manejarError(mensaje, error) {
        console.error(mensaje, error);
        alert(mensaje);
    }

    btnCargar.addEventListener('click', function() {
        cargarImagen();
    });

    function cargarImagen() {
        // Limpiar coordenadas guardadas en el servidor
        fetch('/limpiar-coordenadas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
        })
        .then(response => response.json())
        .then(data => {
            console.log(data.mensaje);
        })
        .catch(error => manejarError('Error al limpiar coordenadas', error));

        // Limpiar la lista de clases
        listaClases.innerHTML = '';
        contenedorResultados.innerHTML = ''; // Limpiar resultados anteriores

        const nombreImagen = selectorImagen.value;
        imagen.src = '/static/imagenes/' + nombreImagen;
        imagen.onload = function() {
            canvas.width = imagen.width;
            canvas.height = imagen.height;
            ctx.drawImage(imagen, 0, 0);
            imagenCargada = true;
        };
        imagen.onerror = function() {
            manejarError('Error al cargar la imagen');
        };
    }

    canvas.addEventListener('mousedown', function(e) {
        if (!imagenCargada) {
            alert("Primero debe cargar una imagen.");
            return;
        }
        const rect = canvas.getBoundingClientRect();
        seleccion.xInicio = e.clientX - rect.left;
        seleccion.yInicio = e.clientY - rect.top;
        seleccionando = true;
    });

    canvas.addEventListener('mousemove', function(e) {
        if (seleccionando) {
            const rect = canvas.getBoundingClientRect();
            seleccion.xFin = e.clientX - rect.left;
            seleccion.yFin = e.clientY - rect.top;
            dibujar();
        }
    });

    canvas.addEventListener('mouseup', function() {
        seleccionando = false;
    });

    function dibujar() {
        ctx.clearRect(0, 0, canvas.width, canvas.height);
        ctx.drawImage(imagen, 0, 0);

        if (seleccion.xInicio != null && seleccion.xFin != null && seleccion.yInicio != null && seleccion.yFin != null) {
            const x = seleccion.xInicio;
            const y = seleccion.yInicio;
            const ancho = seleccion.xFin - seleccion.xInicio;
            const alto = seleccion.yFin - seleccion.yInicio;
            ctx.strokeStyle = 'red';
            ctx.lineWidth = 2;
            ctx.strokeRect(x, y, ancho, alto);
        }
    }

    btnGuardar.addEventListener('click', function() {
        if (!imagenCargada) {
            alert("Primero debe cargar una imagen.");
            return;
        }

        if (seleccion.xInicio == null || seleccion.xFin == null || seleccion.yInicio == null || seleccion.yFin == null) {
            alert("Por favor selecciona una sección antes de guardar.");
            return;
        }

        const x = Math.min(seleccion.xInicio, seleccion.xFin);
        const y = Math.min(seleccion.yInicio, seleccion.yFin);
        const ancho = Math.abs(seleccion.xFin - seleccion.xInicio);
        const alto = Math.abs(seleccion.yFin - seleccion.yInicio);

        if (ancho === 0 || alto === 0) {
            alert("La selección no es válida.");
            return;
        }

        mostrarSeleccionRecortada(x, y, ancho, alto);

        let datos = {
            imagen: selectorImagen.value,
            x: x,
            y: y,
            ancho: ancho,
            alto: alto
        };

        fetch('/guardar-coordenadas', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(datos),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensaje);
        })
        .catch(error => {
            console.error('Error al enviar las coordenadas:', error);
            alert('Error al enviar las coordenadas');
        });
    });

    function mostrarSeleccionRecortada(x, y, ancho, alto) {
        const canvasTemp = document.createElement('canvas');
        const ctxTemp = canvasTemp.getContext('2d');
        canvasTemp.width = ancho;
        canvasTemp.height = alto;

        ctxTemp.drawImage(imagen, x, y, ancho, alto, 0, 0, ancho, alto);

        const imgElemento = document.createElement('img');
        imgElemento.src = canvasTemp.toDataURL('image/png');
        imgElemento.width = 100;

        const fila = document.createElement('tr');

        const celdaClase = document.createElement('td');
        celdaClase.textContent = `Clase ${listaClases.rows.length + 1}`;

        const celdaImagen = document.createElement('td');
        celdaImagen.appendChild(imgElemento);

        fila.appendChild(celdaClase);
        fila.appendChild(celdaImagen);

        listaClases.appendChild(fila);
    }

    function mostrarResultadosAnalisis(data) {
        const contenedorResultados = document.getElementById('contenedorResultados');
        contenedorResultados.innerHTML = ''; // Limpiar resultados anteriores

        // Verificar que haya resultados
        if (!data.resultados || data.resultados.length === 0) {
            contenedorResultados.innerHTML = '<p>No hay resultados para mostrar.</p>';
            return;
        }

        // Crear la tabla completa de resultados
        const table = document.createElement('table');
        table.classList.add('tabla-resultados');

        // Crear el encabezado de la tabla
        const header = document.createElement('tr');
        header.innerHTML = `
            <th>Clase</th>
            <th>Distancia Mahalanobis</th>
            <th>Distancia Euclidiana</th>
            <th>Probabilidad (%)</th>
        `;
        table.appendChild(header);

        // Arrays para almacenar las métricas
        const distanciasMahalanobis = [];
        const distanciasEuclidianas = [];
        const probabilidades = [];

        // Iterar sobre los resultados y agregar filas a la tabla
        data.resultados.forEach((resultado, index) => {
            const row = document.createElement('tr');

            const claseCell = document.createElement('td');
            claseCell.textContent = `Clase ${index + 1}`;

            const mahalaCell = document.createElement('td');
            // Formatear a 4 decimales
            mahalaCell.textContent = resultado.mahalanobis_distance.toFixed(4);
            distanciasMahalanobis.push({ valor: resultado.mahalanobis_distance, clase: index + 1 });

            const euclidCell = document.createElement('td');
            euclidCell.textContent = resultado.euclidean_distance.toFixed(4);
            distanciasEuclidianas.push({ valor: resultado.euclidean_distance, clase: index + 1 });

            const probCell = document.createElement('td');
            // Asumimos que la probabilidad está en el rango 0-100
            if (resultado.probabilidad < 1e-4) {
                probCell.textContent = resultado.probabilidad.toExponential(2);
            } else {
                probCell.textContent = `${resultado.probabilidad.toFixed(2)}%`;
            }
            probabilidades.push({ valor: resultado.probabilidad, clase: index + 1 });

            row.appendChild(claseCell);
            row.appendChild(mahalaCell);
            row.appendChild(euclidCell);
            row.appendChild(probCell);

            table.appendChild(row);
        });

        contenedorResultados.appendChild(table);

        // Calcular las métricas requeridas
        const minMahalanobisObj = distanciasMahalanobis.reduce((min, current) => current.valor < min.valor ? current : min, distanciasMahalanobis[0]);
        const minEuclideanObj = distanciasEuclidianas.reduce((min, current) => current.valor < min.valor ? current : min, distanciasEuclidianas[0]);
        const maxProbabilidadObj = probabilidades.reduce((max, current) => current.valor > max.valor ? current : max, probabilidades[0]);

        // Verificar si cumplen con los umbrales
        const cumpleMahalanobis = minMahalanobisObj.valor < 2.5;
        const cumpleEuclidean = minEuclideanObj.valor < 100;
        const cumpleProbabilidad = maxProbabilidadObj.valor > 75;

        // Crear un contenedor para los resultados destacados
        const contenedorResumen = document.createElement('div');
        contenedorResumen.classList.add('resumen-resultados');

        // Construir el contenido del resumen
        let resumenHTML = '<h3>Clases Destacadas por Criterio:</h3><ul>';

        if (cumpleMahalanobis) {
            resumenHTML += `<li><strong>Distancia Mahalanobis:</strong> Clase ${minMahalanobisObj.clase} (Distancia: ${minMahalanobisObj.valor.toFixed(4)})</li>`;
        } else {
            resumenHTML += `<li><strong>Distancia Mahalanobis:</strong> No cumple con el umbral (< 2.5).</li>`;
        }

        if (cumpleEuclidean) {
            resumenHTML += `<li><strong>Distancia Euclidiana:</strong> Clase ${minEuclideanObj.clase} (Distancia: ${minEuclideanObj.valor.toFixed(4)})</li>`;
        } else {
            resumenHTML += `<li><strong>Distancia Euclidiana:</strong> No cumple con el umbral (< 100).</li>`;
        }

        if (cumpleProbabilidad) {
            resumenHTML += `<li><strong>Probabilidad:</strong> Clase ${maxProbabilidadObj.clase} (Probabilidad: ${maxProbabilidadObj.valor.toFixed(2)}%)</li>`;
        } else {
            resumenHTML += `<li><strong>Probabilidad:</strong> No cumple con el umbral (> 75).</li>`;
        }

        resumenHTML += '</ul>';

        contenedorResumen.innerHTML = resumenHTML;

        // Agregar el resumen al contenedor de resultados
        contenedorResultados.appendChild(contenedorResumen);
    }


    btnAnalizar.addEventListener('click', function() {
        if (!imagenCargada) {
            alert("Primero debe cargar una imagen.");
            return;
        }

        if (seleccion.xInicio == null || seleccion.xFin == null || seleccion.yInicio == null || seleccion.yFin == null) {
            alert("Por favor selecciona una sección antes de analizar.");
            return;
        }

        const x = Math.min(seleccion.xInicio, seleccion.xFin);
        const y = Math.min(seleccion.yInicio, seleccion.yFin);
        const ancho = Math.abs(seleccion.xFin - seleccion.xInicio);
        const alto = Math.abs(seleccion.yFin - seleccion.yInicio);

        if (ancho === 0 || alto === 0) {
            alert("La selección no es válida.");
            return;
        }

        const criterioSeleccionado = selectorCriterio.value;

        let seccionSeleccionada = {
            imagen: selectorImagen.value,
            x: x,
            y: y,
            ancho: ancho,
            alto: alto,
            criterio: criterioSeleccionado
        };

        fetch('/analizar-seccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(seccionSeleccionada),
        })
        .then(response => response.json())
        .then(data => {
            // Llamar a la función para mostrar los resultados en la tabla
            mostrarResultadosAnalisis(data);
            console.log(data);
        })
        .catch(error => manejarError('Error al analizar la sección', error));
    });
});
