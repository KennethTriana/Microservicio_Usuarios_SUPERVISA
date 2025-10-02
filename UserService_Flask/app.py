from dotenv import load_dotenv
import os
from pathlib import Path
from flask import Flask
from sqlalchemy import text
from db import engine
from models import Base
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from flask_restx import Api
from routes import login_ns, usuarios_ns

env_path = Path(__file__).parent / ".env"
load_dotenv(dotenv_path=env_path)

try:
    with engine.connect() as conn:
        conn.execute(text("SELECT 1"))
    print("✅ Conexión a DB exitosa")
except Exception as e:
    print("❌ Error al conectar con la DB:", e)

Base.metadata.create_all(bind=engine)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = os.getenv("JWT_SECRET_KEY", "SUP3RV15A")
jwt = JWTManager(app)

cors_origins = os.getenv("CORS_ORIGINS", "*")
if cors_origins != "*":
    origins = [o.strip() for o in cors_origins.split(",") if o.strip()]
else:
    origins = "*"

CORS(app, resources={r"/*": {"origins": origins}}, supports_credentials=True)

authorizations = {
    "Bearer Auth": {
        "type": "apiKey",
        "in": "header",
        "name": "Authorization",
        "description": "Escribe: Bearer <JWT>"
    }
}

api = Api(
    app,
    version="1.0",
    title="User Service API",
    description="Microservicio de autenticación y gestión de usuarios",
    doc="/docs",
    authorizations=authorizations,
    security="Bearer Auth"
)

api.add_namespace(login_ns, path="/login")
api.add_namespace(usuarios_ns, path="/usuarios")

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("APP_PORT", 5000)))