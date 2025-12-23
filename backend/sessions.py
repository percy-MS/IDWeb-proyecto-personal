import uuid

# Almacenamiento de sesión en memoria
# Formato: { 'token_sesion': { 'user_id': 1, 'nombre': 'Percy', 'email': '...' } }
SESSIONS = {}

def create_session(user_data):
    """Crea una sesión para un usuario y devuelve el ID de sesión."""
    session_id = str(uuid.uuid4())
    SESSIONS[session_id] = user_data
    return session_id

def get_user_from_session(session_id):
    """Devuelve datos de usuario si la sesión es válida, sino None."""
    return SESSIONS.get(session_id)

def delete_session(session_id):
    """Elimina una sesión."""
    if session_id in SESSIONS:
        del SESSIONS[session_id]
