function toggleDescripcion(iconElement) {
    const contenedorPeticion = iconElement.closest('.contenedor-peticion');
    const descripcionElement = contenedorPeticion.querySelector('.descripcion');
    iconElement.classList.toggle('rotar'); // Agregar o quitar la clase 'rotar'
    if (descripcionElement) {
        descripcionElement.classList.toggle('descripcion-visible');
    }
}

function sumarOracion(index) {
    // Realiza una solicitud POST al servidor Flask
    fetch('/sumar_oracion', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/x-www-form-urlencoded',
        },
        body: `index=${index}`,
    })
    .then(response => response.json())
    .then(data => {
        // Maneja la respuesta del servidor, si es necesario
        alert(data.message);
    })
    .catch(error => {
        console.error('Error al enviar la solicitud:', error);
    });
}

function marcarCompleta(index) {
    // Pedir al usuario que ingrese su testimonio
    const testimonio = prompt("Ingresa tu testimonio:");

    if (testimonio !== null) {  // El usuario hizo clic en "Aceptar"
        const xhr = new XMLHttpRequest();
        xhr.open('POST', '/marcar_completa', true);
        xhr.setRequestHeader('Content-Type', 'application/json');

        xhr.onreadystatechange = function () {
            if (xhr.readyState === XMLHttpRequest.DONE) {
                if (xhr.status === 200) {
                    const response = JSON.parse(xhr.responseText);
                    if (response.success) {
                        actualizarInterfaz(response.tareas_actualizadas);
                    } else {
                        console.error('Error al marcar la tarea como completa');
                    }
                }
            }
        };

        xhr.send(JSON.stringify({ index: index, testimonio: testimonio }));
    }
}

function actualizarInterfaz() {
    // Redirigir a la página principal
    window.location.href = '/oracion';
}