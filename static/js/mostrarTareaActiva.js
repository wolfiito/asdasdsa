function toggleDescripcion(iconElement) {
    const contenedorPeticion = iconElement.closest('.contenedor-peticion');
    const descripcionElement = contenedorPeticion.querySelector('.descripcion');
    iconElement.classList.toggle('rotar'); // Agregar o quitar la clase 'rotar'
    if (descripcionElement) {
        descripcionElement.classList.toggle('descripcion-visible');
    }
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