import mysql.connector
from mysql.connector import errorcode
import hashlib
from config import DB_CONFIG

def get_db_connection():
    """Establece y devuelve una conexión a la base de datos."""
    try:
        cnx = mysql.connector.connect(**DB_CONFIG)
        return cnx
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_BAD_DB_ERROR:
            # La base de datos no existe, intentar crearla
            try:
                # Conectar sin base de datos especificada
                temp_config = DB_CONFIG.copy()
                del temp_config['database']
                cnx = mysql.connector.connect(**temp_config)
                cursor = cnx.cursor()
                print(f"La base de datos {DB_CONFIG['database']} no existe. Creándola...")
                cursor.execute(f"CREATE DATABASE {DB_CONFIG['database']} DEFAULT CHARACTER SET 'utf8'")
                cnx.close()
                # Reconectar
                return mysql.connector.connect(**DB_CONFIG)
            except mysql.connector.Error as err2:
                print(f"Falló la creación de la base de datos: {err2}")
                return None
        else:
            print(f"Error conectando a la base de datos: {err}")
            return None

def init_db():
    """Inicializa las tablas base de datos."""
    cnx = get_db_connection()
    if not cnx:
        print("No se pudo conectar a la base de datos para inicializar tablas.")
        return

    cursor = cnx.cursor()

    # Tabla: usuarios
    table_usuarios = (
        "CREATE TABLE IF NOT EXISTS usuarios ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  nombre VARCHAR(100) NOT NULL,"
        "  email VARCHAR(100) NOT NULL UNIQUE,"
        "  password_hash VARCHAR(64) NOT NULL,"
        "  fecha_registro TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ") ENGINE=InnoDB"
    )

    # Tabla: mensajes_contacto
    table_mensajes = (
        "CREATE TABLE IF NOT EXISTS mensajes_contacto ("
        "  id INT AUTO_INCREMENT PRIMARY KEY,"
        "  nombre VARCHAR(100) NOT NULL,"
        "  email VARCHAR(100) NOT NULL,"
        "  asunto VARCHAR(150) NOT NULL,"
        "  mensaje TEXT NOT NULL,"
        "  fecha_envio TIMESTAMP DEFAULT CURRENT_TIMESTAMP"
        ") ENGINE=InnoDB"
    )

    try:
        print("Creando tabla usuarios...")
        cursor.execute(table_usuarios)
        print("Creando tabla mensajes_contacto...")
        cursor.execute(table_mensajes)
        cnx.commit()
        print("Base de datos inicializada correctamente.")
    except mysql.connector.Error as err:
        print(f"Error creando tablas: {err.msg}")
    finally:
        cursor.close()
        cnx.close()

def hash_password(password):
    """Hashea una contraseña usando SHA-256."""
    return hashlib.sha256(password.encode()).hexdigest()

def register_user(nombre, email, password):
    """Registra un nuevo usuario. Devuelve True si es exitoso, False si el email ya existe."""
    cnx = get_db_connection()
    if not cnx:
        return False, "Fallo de conexión a la base de datos"

    cursor = cnx.cursor()
    pwd_hash = hash_password(password)

    try:
        add_user = ("INSERT INTO usuarios "
                    "(nombre, email, password_hash) "
                    "VALUES (%s, %s, %s)")
        data_user = (nombre, email, pwd_hash)
        cursor.execute(add_user, data_user)
        cnx.commit()
        return True, "Usuario creado exitosamente"
    except mysql.connector.Error as err:
        if err.errno == errorcode.ER_DUP_ENTRY:
             return False, "El email ya está registrado"
        return False, str(err)
    finally:
        cursor.close()
        cnx.close()

def check_login(email, password):
    """Verifica credenciales. Devuelve diccionario de usuario si es válido, None si no."""
    cnx = get_db_connection()
    if not cnx:
        return None

    cursor = cnx.cursor(dictionary=True)
    pwd_hash = hash_password(password)

    query = "SELECT id, nombre, email FROM usuarios WHERE email = %s AND password_hash = %s"
    cursor.execute(query, (email, pwd_hash))
    user = cursor.fetchone()
    
    cursor.close()
    cnx.close()
    return user

def save_message(nombre, email, asunto, mensaje):
    """Guarda un mensaje de contacto."""
    cnx = get_db_connection()
    if not cnx:
        return False

    cursor = cnx.cursor()
    try:
        add_msg = ("INSERT INTO mensajes_contacto "
                   "(nombre, email, asunto, mensaje) "
                   "VALUES (%s, %s, %s, %s)")
        data_msg = (nombre, email, asunto, mensaje)
        cursor.execute(add_msg, data_msg)
        cnx.commit()
        return True
    except mysql.connector.Error as err:
        print(f"Error guardando mensaje: {err}")
        return False
    finally:
        cursor.close()
        cnx.close()

def get_all_messages():
    """Obtiene todos los mensajes de contacto para el admin."""
    cnx = get_db_connection()
    if not cnx:
        return []

    cursor = cnx.cursor(dictionary=True)
    query = "SELECT * FROM mensajes_contacto ORDER BY fecha_envio DESC"
    cursor.execute(query)
    messages = cursor.fetchall()
    
    cursor.close()
    cnx.close()
    return messages
