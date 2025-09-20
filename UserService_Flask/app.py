from dotenv import load_dotenv
import os
from pathlib import Path
from flask import Flask
from sqlalchemy import text
from db import engine
from models import Base
from routes import login_bp
from flask_cors import CORS
from flask_jwt_extended import JWTManager

# Cargar variables desde .env
env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

# Probar conexión
try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Conexión a DB exitosa")
except Exception as e:
    print("❌ Error al conectar con la DB:", e)

# Crear tablas si no existen
Base.metadata.create_all(bind=engine)

# Inicializar Flask
app = Flask(__name__)

# Configuración JWT
app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "SUP3RV15A")
jwt = JWTManager(app)   

# Configuración CORS desde variable de entorno
cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins != "*":
    origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
else:
    origins = "*"

CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True)

# Registrar rutas
app.register_blueprint(login_bp)

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("APP_PORT", 5000)))