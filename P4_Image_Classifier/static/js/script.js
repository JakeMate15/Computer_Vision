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

    // Función actualizada para mostrar los resultados del análisis
    function mostrarResultadosAnalisis(data) {
        contenedorResultados.innerHTML = ''; // Limpiar resultados anteriores

        // Crear la tabla
        const table = document.createElement('table');
        table.classList.add('tabla-resultados');

        // Crear el encabezado de la tabla
        const header = document.createElement('tr');
        header.innerHTML = `
            <th>Clase</th>
            <th>Distancia Mahalanobis</th>
            <th>Distancia Euclidiana</th>
            <th>Probabilidad</th>
        `;
        table.appendChild(header);

        // Iterar sobre los resultados y agregar filas a la tabla
        data.resultados.forEach((resultado, index) => {
            const row = document.createElement('tr');

            const claseCell = document.createElement('td');
            claseCell.textContent = `Clase ${index + 1}`;

            const mahalaCell = document.createElement('td');
            // Formatear a 4 decimales
            mahalaCell.textContent = resultado.mahalanobis_distance.toFixed(4);

            const euclidCell = document.createElement('td');
            euclidCell.textContent = resultado.euclidean_distance.toFixed(4);

            const probCell = document.createElement('td');
            // Formatear la probabilidad en notación científica si es muy pequeña
            if (resultado.probabilidad < 1e-4) {
                probCell.textContent = resultado.probabilidad.toExponential(2);
            } else {
                probCell.textContent = resultado.probabilidad.toFixed(6);
            }

            row.appendChild(claseCell);
            row.appendChild(mahalaCell);
            row.appendChild(euclidCell);
            row.appendChild(probCell);

            table.appendChild(row);
        });

        contenedorResultados.appendChild(table);
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
