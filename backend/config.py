import os

# Configuración de Base de Datos
# Usa variables de entorno si existen (para producción/Railway), 
# si no, usa los valores por defecto (para local).

DB_CONFIG = {
    'host': os.environ.get('MYSQLHOST', 'localhost'),
    'user': os.environ.get('MYSQLUSER', 'root'),
    'password': os.environ.get('MYSQLPASSWORD', 'root'),
    'database': os.environ.get('MYSQLDATABASE', 'mandolin_db'),
    'port': int(os.environ.get('MYSQLPORT', 3306))
}
