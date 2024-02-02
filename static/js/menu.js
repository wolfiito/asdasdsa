const cloud = document.getElementById("cloud");
const barraLateral = document.querySelector(".barra-lateral");
const spans = document.querySelectorAll("span");
const palanca = document.querySelector(".switch");
const circulo = document.querySelector(".circulo");
const menu = document.querySelector(".menu");
const main = document.querySelector("main");

// Recuperar el estado del modo oscuro desde el almacenamiento local
const isDarkMode = localStorage.getItem("darkMode") === "true";

// Función para activar o desactivar el modo oscuro
const toggleDarkMode = () => {
    let body = document.body;
    body.classList.toggle("dark-mode");

    // Guardar el estado del modo oscuro en el almacenamiento local
    const currentMode = body.classList.contains("dark-mode") ? "true" : "false";
    localStorage.setItem("darkMode", currentMode);

    circulo.classList.toggle("prendido");
};

// Aplicar el modo oscuro si estaba activo antes
if (isDarkMode) {
    toggleDarkMode();
}

menu.addEventListener("click", () => {
    document.getElementById('cloud').style.display = 'none';
    barraLateral.classList.toggle("max-barra-lateral");
    if (barraLateral.classList.contains("max-barra-lateral")) {
        menu.children[0].style.display = "none";
        menu.children[1].style.display = "block";
        menu.style.backgroundColor = "var(--color-boton-circulo)";
        menu.style.color = "var(--color-circulo)";
    } else {
        menu.children[0].style.display = "block";
        menu.children[1].style.display = "none";
        menu.style.backgroundColor = "var(--color-circulo)";
        menu.style.color = "var(--color-boton-circulo)";
    }
    // if (window.innerWidth <= 320) {
    //     barraLateral.classList.add("mini-barra-lateral");
    //     main.classList.add("min-main");
    //     spans.forEach((span) => {
    //         span.classList.add("oculto");
    //     });
    // }
});

palanca.addEventListener("click", toggleDarkMode);

cloud.addEventListener("click", () => {
    barraLateral.classList.toggle("mini-barra-lateral");
    main.classList.toggle("min-main");
    spans.forEach((span) => {
        span.classList.toggle("oculto");
    });
});