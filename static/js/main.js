document.addEventListener('DOMContentLoaded', () => {
    // Menú móvil
    const hamburger = document.querySelector('.hamburger');
    const navLinks = document.querySelector('.nav-links');

    if (hamburger) {
        hamburger.addEventListener('click', () => {
            navLinks.classList.toggle('active');
            hamburger.classList.toggle('active');

            // Animación simple para barras (opcional, CSS maneja la mayoría)
        });
    }

    // Resaltar enlace activo
    const currentPath = window.location.pathname;
    const links = document.querySelectorAll('.nav-links a');

    links.forEach(link => {
        // Verificar si el href coincide con el final de la ruta actual
        const href = link.getAttribute('href');
        // Verificación simple: si la ruta actual termina con el href
        if (currentPath.includes(href) && href !== '/') {
            link.classList.add('active');
        } else if (href === '/' && (currentPath === '/' || currentPath === '/index.html' || currentPath.endsWith('/frontend/'))) {
            // Verificación de página de inicio
            link.classList.add('active');
        }
    });

    console.log('JS Principal cargado.');
});
