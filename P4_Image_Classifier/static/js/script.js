document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const btnCargar = document.getElementById('btnCargar');
    const btnGuardar = document.getElementById('btnGuardar');
    const btnAnalizar = document.getElementById('btnAnalizar');
    const selectorImagen = document.getElementById('selectorImagen');
    const listaClases = document.getElementById('listaClases');

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

        const x = seleccion.xInicio;
        const y = seleccion.yInicio;
        const ancho = seleccion.xFin - seleccion.xInicio;
        const alto = seleccion.yFin - seleccion.yInicio;
        ctx.strokeStyle = 'red';
        ctx.lineWidth = 2;
        ctx.strokeRect(x, y, ancho, alto);
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

    btnAnalizar.addEventListener('click', function() {
        if (!imagenCargada) {
            alert("Primero debe cargar una imagen.");
            return;
        }

        if (!seleccion.xInicio || !seleccion.xFin || !seleccion.yInicio || !seleccion.yFin) {
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

        let seccionSeleccionada = {
            imagen: selectorImagen.value,
            x: x,
            y: y,
            ancho: ancho,
            alto: alto
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
            alert(data.mensaje);
            if (data.resultado) {
                let resultadoImg = new Image();
                resultadoImg.src = '/' + data.resultado;
                resultadoImg.onload = function() {
                    ctx.drawImage(resultadoImg, 0, 0);
                };
            }
        })
        .catch(error => manejarError('Error al analizar la sección', error));
    });
});
