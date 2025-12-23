# Proyecto: MandoLearn

**URL del Proyecto:** [http://idweb-proyecto-personal-production.up.railway.app/](http://idweb-proyecto-personal-production.up.railway.app/)

## Descripción
Este es el proyecto final para el curso de Introducción al Desarrollo Web. Es un sitio web educativo dedicado a la enseñanza de la mandolina, que incluye secciones de teoría musical, ejercicios interactivos y una breve historia del instrumento. La aplicación cuenta con funcionalidades completas de registro de usuarios, inicio de sesión seguro, gestión de sesiones y un formulario de contacto con panel de administración protegido.

## Lenguajes y Tecnologías
*   **HTML5** (Estructura)
*   **CSS3** (Estilos y Diseño Responsivo)
*   **JavaScript** (Lógica del Frontend)
*   **Python** (Backend y Lógica del Servidor)
*   **SQL** (Base de Datos MySQL)
*   **Librerías:** `mysql-connector-python`

## Estructura del Proyecto

*   `/frontend`: Archivos HTML.
*   `/static`: Archivos CSS, JS e imágenes.
*   `/backend`: Código del servidor Python y lógica de base de datos.

## Requisitos Previos

1.  Tener **Python 3** instalado.
2.  Tener **MySQL Server** instalado y corriendo.
3.  Instalar las dependencias:
    ```bash
    pip install -r requirements.txt
    ```

## Configuración

1.  Abre el archivo `backend/config.py`.
2.  Asegúrate de que el usuario y la contraseña de MySQL sean correctos:
    ```python
    DB_CONFIG = {
        'host': 'localhost',
        'user': 'root',
        'password': 'root',  # <--- Cambia esto si tu password es diferente
        'database': 'mandolin_db'
    }
    ```
    *Nota: El sistema creará la base de datos `mandolin_db` automáticamente la primera vez.*

## Cómo Ejecutar el Proyecto

1.  Abre una terminal en la carpeta principal del proyecto (`IDWeb-proyecto_personal`).
2.  Ejecuta el servidor:
    ```bash
    python backend/server.py
    ```
3.  Abre tu navegador y entra a:
    http://localhost:8000

## Funcionalidades para Probar

*   **Página de Inicio y Contenido:** Navega por las secciones de Teoría, Ejercicios, etc.
*   **Registro:** Crea una cuenta nueva en `/registro.html`.
*   **Login:** Inicia sesión para acceder a funciones protegidas.
*   **Contacto:** Envía un mensaje desde `/contacto.html`.
*   **Panel Admin:** (Requiere Login) Ve a `/admin/mensajes` para ver los mensajes enviados.

---
Creado por: Percy Molina
