import os
from dotenv import load_dotenv

# Carga el archivo .env desde la ruta del proyecto
load_dotenv()

DB_SERVER = os.getenv("DB_SERVER")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_NAME = os.getenv("DB_NAME")

# Debug para confirmar que se leen
print("🔍 DB_SERVER:", DB_SERVER)
print("🔍 DATABASE_URL:", f"mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}")

DATABASE_URL = f"mssql+pymssql://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
APP_PORT = int(os.getenv("APP_PORT", 5000))