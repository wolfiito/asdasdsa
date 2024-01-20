// Arreglo con las 30 frases sobre la oración y sus versículos
var frasesOracion = [
    { frase: "La oración es el lenguaje del alma.", versiculo: "Salmo 19:14 (RVR1960)", texto:'Sean gratas las palabras de mi boca y la meditación de mi corazón delante de ti, oh Jehová, roca mía, y redentor mío.'},
    { frase: "La oración es el camino hacia la paz interior.", versiculo: "Filipenses 4:7 (NVI)", texto:'Y la paz de Dios, que sobrepasa todo entendimiento, cuidará vuestros corazones y vuestros pensamientos en Cristo Jesús.'},
    { frase: "La oración es un diálogo con lo divino.", versiculo: "Jeremías 33:3 (RVR1960)", texto:'Clama a mí, y yo te responderé, y te enseñaré cosas grandes y ocultas que tú no conoces.'},
    { frase: "La oración es el camino hacia el poder de Dios.", versiculo: "Lucas 11:9 (NVI)", texto:'Así que les digo: pidan, y se les dará; busquen, y encontrarán; llamen, y se les abrirá.'},
    { frase: "La oración es el antídoto contra la ansiedad.", versiculo: "Filipenses 4:6 (RVR1960)", texto:'Por nada estéis afanosos, sino sean conocidas vuestras peticiones delante de Dios en toda oración y ruego, con acción de gracias.'},
    { frase: "La oración es la puerta al poder de Dios.", versiculo: "Mateo 7:7 (NVI)", texto:'Pidan, y se les dará; busquen, y encontrarán; llamen, y se les abrirá.'},
    { frase: "La oración es un refugio en tiempos de tribulación.", versiculo: "Salmo 34:17 (RVR1960)", texto:'Claman los justos, y Jehová oye, y los libra de todas sus angustias.'},
    { frase: "La oración es la conexión con la sabiduría divina.", versiculo: "Santiago 1:5 (NVI)", texto:'Y si a alguno de ustedes le falta sabiduría, pídasela a Dios, y él se la dará, pues Dios da a todos generosamente sin menospreciar a nadie.'},
    { frase: "La oración es la forma de buscar la dirección de Dios.", versiculo: "Proverbios 3:5-6 (RVR1960)", texto:'Confía en Jehová con todo tu corazón y no te apoyes en tu propia prudencia. Reconócelo en todos tus caminos, y él enderezará tus veredas.'},
    { frase: "La oración es el lazo que une al creyente con Dios.", versiculo: "Juan 15:7 (NVI)", texto:'Si permanecen en mí, y mis palabras permanecen en ustedes, pidan lo que quieran, y se les concederá.'},
    { frase: "La oración es el acto de confiar en el plan de Dios.", versiculo: "Romanos 8:28 (RVR1960)", texto:'Y sabemos que a los que aman a Dios, todas las cosas les ayudan a bien.'},
    { frase: "La oración es el alimento del alma.", versiculo: "Mateo 6:11 (NVI)", texto:'Danos hoy el pan nuestro de cada día.'},
    { frase: "La oración es el camino hacia la sanidad espiritual.", versiculo: "Santiago 5:16 (RVR1960)", texto:'Confesaos vuestras ofensas unos a otros, y orad unos por otros, para que seáis sanados.'},
    { frase: "La oración es la respuesta a la soledad.", versiculo: "Hebreos 13:5 (NVI)", texto:'Manténganse libres del amor al dinero, y conténtense con lo que tienen, porque Dios ha dicho: \'Nunca te dejaré; jamás te desampararé.\''},
    { frase: "La oración es el refugio en tiempos de prueba.", versiculo: "1 Pedro 5:7 (RVR1960)", texto:'Echando toda vuestra ansiedad sobre él, porque él tiene cuidado de vosotros.'},
    { frase: "La oración es la comunicación con el Creador.", versiculo: "Jeremías 29:12 (NVI)", texto:'Entonces me invocarán, y vendrán a suplicarme, y yo los escucharé.'},
    { frase: "La oración es el puente a la esperanza.", versiculo: "Romanos 12:12 (RVR1960)", texto:'Gozaos en la esperanza; estad firmes en la tribulación; perseverad en la oración.'},
    { frase: "La oración es la fortaleza en la debilidad.", versiculo: "2 Corintios 12:9 (NVI)", texto:'Pero él me dijo: \'Te basta con mi gracia, pues mi poder se perfecciona en la debilidad.\''},
    { frase: "La oración es el acto de agradecer a Dios.", versiculo: "1 Tesalonicenses 5:18 (RVR1960)", texto:'Dad gracias en todo, porque esta es la voluntad de Dios para con vosotros en Cristo Jesús.'},
    { frase: "La oración es la demostración de fe.", versiculo: "Marcos 11:24 (NVI)", texto:'Por eso les digo: Crean que ya han recibido todo lo que estén pidiendo en oración, y lo obtendrán.'},
    { frase: "La oración es la fuente de la paciencia.", versiculo: "Romanos 8:25 (RVR1960)", texto:'Pero si esperamos lo que no vemos, con paciencia lo aguardamos.'},
    { frase: "La oración es el acto de buscar la dirección de Dios.", versiculo: "Mateo 6:33 (NVI)", texto:'Más bien, busquen primeramente el reino de Dios y su justicia, y todas estas cosas les serán añadidas.'},
    { frase: "La oración es el camino a la reconciliación con Dios.", versiculo: "2 Corintios 5:18 (NVI)", texto:'Y todo esto proviene de Dios, quien nos reconcilió consigo mismo por Cristo, y nos dio el ministerio de la reconciliación.'},
    { frase: "La oración es el fundamento de una vida cristiana sólida.", versiculo: "Colosenses 4:2 (NVI)", texto:'Perseveren en la oración, manténganse alerta y sean agradecidos.'}
];

// Función para seleccionar una frase aleatoria
function obtenerFraseAleatoria() {
    var indiceAleatorio = Math.floor(Math.random() * frasesOracion.length);
    return frasesOracion[indiceAleatorio];
}

// Función para actualizar la sección "texto" con una frase aleatoria
function actualizarTextoAleatorio() {
    var fraseAleatoria = obtenerFraseAleatoria();
    document.querySelector(".texto span").textContent = fraseAleatoria.frase;
    document.querySelector(".texto .text").textContent = fraseAleatoria.texto;
    document.querySelector(".texto .versiculo").textContent = fraseAleatoria.versiculo
}

// Llama a la función para actualizar la frase al cargar la página
window.onload = actualizarTextoAleatorio;
