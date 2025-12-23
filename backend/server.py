import http.server
import socketserver
import os
import urllib.parse
import json
import db
import sessions
import sys
from http import cookies

# Configuración
PORT = 8000
# Aseguramos que estamos sirviendo desde la raíz del proyecto
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
FRONTEND_DIR = os.path.join(PROJECT_ROOT, 'frontend')
STATIC_DIR = os.path.join(PROJECT_ROOT, 'static')

class MandolinRequestHandler(http.server.SimpleHTTPRequestHandler):
    
    def do_GET(self):
        """Maneja las peticiones GET para páginas y archivos estáticos."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        # 1. Archivos Estáticos (CSS, JS, Imágenes)
        if path.startswith('/static/'):
            # Servir desde el directorio static
            # Eliminar el prefijo '/static/' para encontrar la ruta real
            file_path = os.path.join(STATIC_DIR, path[8:]) 
            if os.path.exists(file_path) and os.path.isfile(file_path):
                self.serve_file(file_path)
            else:
                self.send_error(404, "Static file not found")
            return

        # 2. Ruta de Admin Protegida
        if path == '/admin/mensajes' or path == '/admin/mensajes.html':
            if self.is_authenticated():
                # Servir página de admin
                file_path = os.path.join(FRONTEND_DIR, 'admin_mensajes.html')
                if os.path.exists(file_path):
                     # Servimos el HTML y usamos JS para obtener los mensajes
                     self.serve_file(file_path)
                else:
                    self.send_error(404, "Página de admin no encontrada")
            else:
                # Redirigir al login
                self.send_response(302)
                self.send_header('Location', '/login.html')
                self.end_headers()
            return

        # 3. Páginas HTML
        # Mapear / a index.html
        if path == '/' or path == '/index.html':
            self.serve_file(os.path.join(FRONTEND_DIR, 'index.html'))
            return
        
        # Manejo genérico para archivos .html en frontend
        if path.endswith('.html'):
            clean_path = path.lstrip('/')
            file_path = os.path.join(FRONTEND_DIR, clean_path)
            if os.path.exists(file_path):
                self.serve_file(file_path)
                return
            else:
                self.send_error(404, "Página no encontrada")
                return

        # Por defecto: 404
        self.send_error(404, "Archivo no encontrado")

    def do_POST(self):
        """Maneja las peticiones POST para formularios (API)."""
        parsed_path = urllib.parse.urlparse(self.path)
        path = parsed_path.path

        if path == '/api/registro':
            self.handle_register()
        elif path == '/api/login':
            self.handle_login()
        elif path == '/api/contacto':
            self.handle_contact()
        elif path == '/api/logout':
            self.handle_logout()
        elif path == '/api/mensajes': # API Admin para obtener mensajes
             self.handle_get_messages()
        else:
            self.send_error(404, "Endpoint API no encontrado")

    def serve_file(self, file_path):
        """Ayudante para servir un archivo con el tipo MIME correcto."""
        try:
            with open(file_path, 'rb') as f:
                content = f.read()
            
            self.send_response(200)
            
            # Adivinanza simple de tipo MIME
            if file_path.endswith('.css'):
                self.send_header('Content-Type', 'text/css')
            elif file_path.endswith('.js'):
                self.send_header('Content-Type', 'application/javascript')
            elif file_path.endswith('.html'):
                self.send_header('Content-Type', 'text/html')
            elif file_path.endswith('.png'):
                self.send_header('Content-Type', 'image/png')
            elif file_path.endswith('.jpg') or file_path.endswith('.jpeg'):
                self.send_header('Content-Type', 'image/jpeg')
            
            self.send_header('Content-Length', len(content))
            self.end_headers()
            self.wfile.write(content)
        except Exception as e:
            print(f"Error sirviendo archivo: {e}")
            self.send_error(500, "Error Interno del Servidor")

    def get_post_data(self):
        """Lee y parsea datos POST (form-urlencoded)."""
        content_length = int(self.headers.get('Content-Length', 0))
        post_body = self.rfile.read(content_length).decode('utf-8')
        # Devuelve un dict: {'clave': ['valor'], ...} -> aplanar a {'clave': 'valor'}
        data = urllib.parse.parse_qs(post_body)
        return {k: v[0] for k, v in data.items()}

    def handle_register(self):
        data = self.get_post_data()
        nombre = data.get('nombre')
        email = data.get('email')
        password = data.get('password')
        confirm = data.get('confirm_password')

        if not (nombre and email and password):
            self.send_error(400, "Missing fields")
            return
        
        if password != confirm:
            self.send_error(400, "Passwords do not match")
            return

        success, message = db.register_user(nombre, email, password)
        
        if success:
            # Redirigir al login
            self.send_response(302)
            self.send_header('Location', '/login.html')
            self.end_headers()
        else:
            # Mostrar error (respuesta de texto simple por ahora)
            self.send_response(400)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write(f"<h1>Error: {message}</h1><a href='/registro.html'>Volver</a>".encode('utf-8'))

    def handle_login(self):
        data = self.get_post_data()
        email = data.get('email')
        password = data.get('password')

        user = db.check_login(email, password)
        
        if user:
            # Crear sesión
            session_id = sessions.create_session(user)
            
            # Establecer cookie
            c = cookies.SimpleCookie()
            c['session_id'] = session_id
            c['session_id']['path'] = '/'
            c['session_id']['httponly'] = True 
            
            self.send_response(302)
            for header_line in c.output().splitlines():
                 self.send_header('Set-Cookie', header_line.split(': ')[1])
            self.send_header('Location', '/index.html')
            self.end_headers()
        else:
            self.send_response(401)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>Credenciales inválidas</h1><a href='/login.html'>Intentar de nuevo</a>".encode('utf-8'))

    def handle_contact(self):
        data = self.get_post_data()
        nombre = data.get('nombre')
        email = data.get('email')
        asunto = data.get('asunto')
        mensaje = data.get('mensaje')

        if db.save_message(nombre, email, asunto, mensaje):
            # Página de éxito o redirección
            self.send_response(200)
            self.send_header('Content-Type', 'text/html; charset=utf-8')
            self.end_headers()
            self.wfile.write("<h1>Mensaje enviado correctamente!</h1><a href='/index.html'>Volver al inicio</a>".encode('utf-8'))
        else:
            self.send_error(500, "Error guardando el mensaje")

    def handle_logout(self):
        # Limpiar sesión
        cookie_header = self.headers.get('Cookie')
        if cookie_header:
            c = cookies.SimpleCookie(cookie_header)
            if 'session_id' in c:
                sid = c['session_id'].value
                sessions.delete_session(sid)
        
        self.send_response(302)
        # Expirar cookie
        self.send_header('Set-Cookie', 'session_id=; Path=/; Expires=Thu, 01 Jan 1970 00:00:00 GMT')
        self.send_header('Location', '/login.html')
        self.end_headers()

    def handle_get_messages(self):
        # Verificación de API
        if not self.is_authenticated():
            self.send_error(401, "No autorizado")
            return

        msgs = db.get_all_messages()
        # Convertir objetos datetime a string
        for m in msgs:
            if 'fecha_envio' in m:
                m['fecha_envio'] = str(m['fecha_envio'])

        self.send_response(200)
        self.send_header('Content-Type', 'application/json')
        self.end_headers()
        self.wfile.write(json.dumps(msgs).encode('utf-8'))

    def is_authenticated(self):
        cookie_header = self.headers.get('Cookie')
        if not cookie_header:
            return False
        c = cookies.SimpleCookie(cookie_header)
        if 'session_id' not in c:
            return False
        sid = c['session_id'].value
        user = sessions.get_user_from_session(sid)
        return user is not None

if __name__ == "__main__":
    # Inicializar Base de Datos
    print("Inicializando Base de Datos...")
    db.init_db()
    
    print(f"Iniciando servidor en http://localhost:{PORT}")
    try:
        with socketserver.TCPServer(("", PORT), MandolinRequestHandler) as httpd:
            print("Servidor corriendo. Presiona Ctrl+C para detener.")
            httpd.serve_forever()
    except KeyboardInterrupt:
        print("\nDeteniendo servidor...")
