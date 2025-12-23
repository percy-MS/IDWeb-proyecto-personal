import mysql.connector
import os
from dotenv import load_dotenv

# Cargar variables
load_dotenv()

print("--- DIAGNÓSTICO DE CONEXIÓN ---")
print(f"Host: {os.environ.get('MYSQLHOST')}")
print(f"User: {os.environ.get('MYSQLUSER')}")
print(f"Port: {os.environ.get('MYSQLPORT')}")
print(f"DB: {os.environ.get('MYSQLDATABASE')}")

try:
    print("\nIntentando conectar...")
    cnx = mysql.connector.connect(
        host=os.environ.get('MYSQLHOST'),
        user=os.environ.get('MYSQLUSER'),
        password=os.environ.get('MYSQLPASSWORD'),
        database=os.environ.get('MYSQLDATABASE'),
        port=int(os.environ.get('MYSQLPORT', 3306))
    )
    print("¡CONEXIÓN EXITOSA!")
    cnx.close()
except Exception as e:
    print(f"\nFALLO LA CONEXIÓN:\n{e}")
