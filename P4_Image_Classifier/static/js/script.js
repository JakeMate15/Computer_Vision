document.addEventListener('DOMContentLoaded', function() {
    const canvas = document.getElementById('canvas');
    const ctx = canvas.getContext('2d');
    const btnCargar = document.getElementById('btnCargar');
    const btnGuardar = document.getElementById('btnGuardar');
    const btnAnalizar = document.getElementById('btnAnalizar');
    const selectorImagen = document.getElementById('selectorImagen');

    let imagen = new Image();
    let seleccion = {};
    let seleccionando = false;

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
        .catch(error => {
            console.error('Error al limpiar coordenadas:', error);
            alert('Hubo un error al limpiar las coordenadas');
        });
    
        let nombreImagen = selectorImagen.value;
        console.log("Imagen seleccionada:", nombreImagen); 
        imagen.src = '/static/imagenes/' + nombreImagen;
        imagen.onload = function() {
            canvas.width = imagen.width;
            canvas.height = imagen.height;
            ctx.drawImage(imagen, 0, 0);
        }
    }

    canvas.addEventListener('mousedown', function(e) {
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
        const x = Math.min(seleccion.xInicio, seleccion.xFin);
        const y = Math.min(seleccion.yInicio, seleccion.yFin);
        const ancho = Math.abs(seleccion.xFin - seleccion.xInicio);
        const alto = Math.abs(seleccion.yFin - seleccion.yInicio);
    
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
            console.error('Error:', error);
            alert('Error al enviar las coordenadas');
        });
    });
    

    btnAnalizar.addEventListener('click', function() {
        // Verificar si una sección ha sido seleccionada
        if (!seleccion.xInicio || !seleccion.xFin || !seleccion.yInicio || !seleccion.yFin) {
            alert("Por favor selecciona una sección antes de analizar.");
            return;
        }
    
        // Obtener las coordenadas de la sección seleccionada
        const x = Math.min(seleccion.xInicio, seleccion.xFin);
        const y = Math.min(seleccion.yInicio, seleccion.yFin);
        const ancho = Math.abs(seleccion.xFin - seleccion.xInicio);
        const alto = Math.abs(seleccion.yFin - seleccion.yInicio);
    
        // Crear un objeto que contenga la información de la sección seleccionada
        let seccionSeleccionada = {
            imagen: selectorImagen.value,
            x: x,
            y: y,
            ancho: ancho,
            alto: alto
        };
    
        // Enviar la sección seleccionada al servidor para análisis
        fetch('/analizar-seccion', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify(seccionSeleccionada),
        })
        .then(response => response.json())
        .then(data => {
            alert(data.mensaje);  // Muestra un mensaje de éxito
            if (data.resultado) {
                let resultadoImg = new Image();
                resultadoImg.src = '/' + data.resultado;
                resultadoImg.onload = function() {
                    ctx.drawImage(resultadoImg, 0, 0);  // Mostrar imagen resultante del análisis en el canvas
                }
            }
        })
        .catch(error => {
            console.error('Error al analizar la sección:', error);
            alert('Hubo un error durante el análisis');
        });
    });
    
});
