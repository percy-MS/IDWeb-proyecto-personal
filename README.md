# Proyecto: MandoLearn

**URL del Proyecto:** [https://idweb-proyecto-personal-production.up.railway.app/](https://idweb-proyecto-personal-production.up.railway.app/)

## Descripción
MandoLearn es una plataforma web educativa diseñada para la enseñanza de la mandolina. El proyecto ofrece recursos teóricos, ejercicios prácticos y una reseña histórica del instrumento. Funcionalmente, la aplicación permite el registro y autenticación de usuarios, gestión de sesiones seguras y cuenta con un sistema de contacto que incluye un panel de administración protegido para visualizar los mensajes recibidos.

## Lenguajes y Tecnologías
Este proyecto fue desarrollado utilizando las siguientes tecnologías:

*   **HTML** (Estructura semántica del contenido)
*   **CSS** (Estilos y diseño responsivo)
*   **JS** (Lógica del lado del cliente e interactividad)
*   **Python** (Backend y lógica del servidor)
*   **SQL** (Gestión de base de datos MySQL)

## Estructura del Proyecto

*   `/frontend`: Archivos HTML.
*   `/static`: Archivos CSS, JS e imágenes.
*   `/backend`: Código del servidor Python y lógica de base de datos.

## Instalación y Ejecución Local

1.  **Requisitos**: Python 3 y MySQL instalados.
2.  **Instalar dependencias**:
    ```bash
    pip install -r requirements.txt
    ```
3.  **Configurar Base de Datos**:
    El sistema utiliza variables de entorno. Crea un archivo `.env` o configura tus variables de sistema. Si no existen, por defecto intentará conectar a `localhost` con usuario `root`.
4.  **Ejecutar Servidor**:
    ```bash
    python backend/server.py
    ```
5.  **Acceder**: Visita `http://localhost:8000`

---
Creado por: Percy Molina
