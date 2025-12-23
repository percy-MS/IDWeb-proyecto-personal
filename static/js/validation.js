document.addEventListener('DOMContentLoaded', () => {
    const forms = document.querySelectorAll('form');

    forms.forEach(form => {
        form.addEventListener('submit', (e) => {
            let isValid = true;

            // Limpiar errores previos
            form.querySelectorAll('.error-message').forEach(el => el.style.display = 'none');
            form.querySelectorAll('.input-error').forEach(el => el.classList.remove('input-error'));

            // Validar basado en tipo de input y atributos
            const inputs = form.querySelectorAll('input, textarea');

            inputs.forEach(input => {
                if (input.hasAttribute('required') && !input.value.trim()) {
                    showError(input, 'Este campo es obligatorio.');
                    isValid = false;
                }

                if (input.type === 'email' && input.value) {
                    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
                    if (!emailRegex.test(input.value)) {
                        showError(input, 'Por favor ingresa un email válido.');
                        isValid = false;
                    }
                }

                if (input.type === 'password' && input.value) {
                    if (input.value.length < 6) {
                        showError(input, 'La contraseña debe tener al menos 6 caracteres.');
                        isValid = false;
                    }
                }

                // Verificación de Confirmar Contraseña
                if (input.name === 'confirm_password') {
                    const passwordInput = form.querySelector('input[name="password"]');
                    if (passwordInput && input.value !== passwordInput.value) {
                        showError(input, 'Las contraseñas no coinciden.');
                        isValid = false;
                    }
                }
            });

            if (!isValid) {
                e.preventDefault(); // Detener envío si validación falla
            }
        });
    });
});

function showError(input, message) {
    const formGroup = input.closest('.form-group');
    let errorDisplay = formGroup.querySelector('.error-message');

    // Crear elemento de mensaje de error si no existe
    if (!errorDisplay) {
        errorDisplay = document.createElement('small');
        errorDisplay.className = 'error-message';
        formGroup.appendChild(errorDisplay);
    }

    input.classList.add('input-error');
    errorDisplay.innerText = message;
    errorDisplay.style.display = 'block';
}
