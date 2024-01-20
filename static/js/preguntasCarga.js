function mostrarContenido(element) {
    var contenidoSpan = element.querySelector('.contenido');
    var contenidoValue = contenidoSpan.textContent.trim();

    console.log("Contenido enviado:", contenidoValue);

    // Enviar el contenido al servidor Flask usando Axios
    axios.get('/procesar_voto', {
        params: {
            pregunta: contenidoValue
        }
    })
    .then(function(response) {
        // Manejar la respuesta del servidor si es necesario
        console.log(response.data);
        // Recarga la página después de 50 ms
        setTimeout(function () {
            location.reload();
        }, 50);
    })
    .catch(function(error) {
        // Manejar errores si es necesario
        console.error(error);
    });
}


function enviarPregunta(event) {
    event.preventDefault();

    var preguntaInput = document.getElementById('pregunta');
    var nuevaPregunta = preguntaInput.value.trim();

    if (nuevaPregunta !== '') {
        axios.post('/procesar_pregunta', { pregunta: nuevaPregunta })
            .then(function (response) {
                console.log(response.data);
                // Recarga la página después de 50 ms
                setTimeout(function () {
                    location.reload();
                }, 50);
            })
            .catch(function (error) {
                console.error(error);
            });
    }
}
