function mostrarContenido(opcion) {

    console.log('Estas enviando', opcion)
    var contenidoDerecha = document.querySelector('.seleccion-menu');
    // Limpia el contenido actual de la sección "derecha"
    contenidoDerecha.innerHTML = '';

    // Carga el contenido HTML desde archivos externos según la opción seleccionada
    if (opcion === 'oracion') {
        cargarContenidoDesdeArchivo('/oracion');
    } else if (opcion === 'horaSilenciosa') {
        cargarContenidoDesdeArchivo('/hora_silenciosa');
    } else if (opcion === 'respuestaPeticiones') {
        cargarContenidoDesdeArchivo('templates/peticionesRespondidas.html');
    } 
    // Agrega más condiciones para otras opciones según sea necesario
}

function cargarContenidoDesdeArchivo(archivo) {
    var contenidoDerecha = document.querySelector('.seleccion-menu');
    var xhr = new XMLHttpRequest();

    xhr.onreadystatechange = function() {
        if (xhr.readyState === 4 && xhr.status === 200) {
            contenidoDerecha.innerHTML = xhr.responseText;
        }
    };

    xhr.open('GET', archivo, true);
    xhr.send();
}
