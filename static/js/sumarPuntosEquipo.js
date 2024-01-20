function sumarPuntos(opcion) {
    let puntos = prompt('Cuántos puntos quieres dar: ');

    if (opcion === "CB+") {
        enviarPuntos("CB+", puntos);
    } else if (opcion === "CB-") {
        enviarPuntos("CB-", puntos);
    } else if (opcion === "CP+") {
        enviarPuntos("CP+", puntos);
    } else if (opcion === "CP-") {
        enviarPuntos("CP-", puntos);
    }
}

function enviarPuntos(opcion, puntos) {
    fetch('/ruta-en-tu-servidor-flask', {
        method: 'POST',
        headers: {
            'Content-Type': 'application/json'
        },
        body: JSON.stringify({
            opcion: opcion,
            puntos: puntos
        })
    })
    .then(response => {
        if (!response.ok) {
            throw new Error('Error al enviar puntos al servidor');
        }
        // Manejar la respuesta del servidor si es necesario
        return response.json();
    })
    .then(data => {
        // Hacer algo con la respuesta del servidor si es necesario
        console.log('Respuesta del servidor:', data);
        actualizarMarcador(data, opcion)
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

function actualizarMarcador(data, opcion) {
    // Actualiza los puntos en el marcador según la respuesta del servidor
    var puntosElement;
    if (opcion === "CB+") {
        puntosElement = document.getElementById('puntos-equipo-barrio');
        console.log("Barrio",puntosElement)
    } else if (opcion === "CB-") {
        puntosElement = document.getElementById('puntos-equipo-barrio');
        console.log("Barrio",puntosElement)
    } else if (opcion === "CP+") {
        puntosElement = document.getElementById('puntos-equipo-poderosas');
        console.log("Poderosas",puntosElement)
    } else if (opcion === "CP-") {
        puntosElement = document.getElementById('puntos-equipo-poderosas');
        console.log("Poderosas",puntosElement)
    }

    // Verifica si el elemento existe antes de intentar modificar su contenido
    if (puntosElement) {
        console.log(data)
        // Actualiza el contenido del elemento con los nuevos puntos del equipo
        puntosElement.innerText = data;
    } else {
        console.error('Elemento no encontrado: puntos-equipo');
    }
}