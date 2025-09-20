from flask import Blueprint, request, jsonify
from db import SessionLocal
from datetime import datetime, timedelta
from pytz import timezone
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity

login_bp = Blueprint("login_bp", __name__)

# Login
@login_bp.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    login_user = data.get("login")
    password_user = data.get("password")

    if not login_user or not password_user:
        return jsonify({"error": "Usuario y contraseña requeridos"}), 400

    session = SessionLocal()
    try:
        # Buscar usuario
        user = session.query(User).filter(
            User.login == login_user,
            User.password == password_user
        ).first()

        if not user:
            return jsonify({"error": "Credenciales inválidas"}), 401

        # Obtener hora en Colombia y ajustar +1 hora
        now_colombia = datetime.now(timezone("America/Bogota")) + timedelta(hours=1)
        user.fec_ult_entrada = now_colombia
        session.commit()

        # Generar token con expiración de 24 horas
        access_token = create_access_token(
            identity={"id": str(user.id), "login": user.login},
            expires_delta=timedelta(hours=24)
        )

        return jsonify({
            "message": "Login exitoso",
            "token": access_token,
            "usuario": {
                "id": str(user.id),
                "nom_usuario": user.nom_usuario,
                "login": user.login,
                "fec_ult_entrada": now_colombia.strftime("%Y-%m-%d %H:%M:%S")
            }
        })
    finally:
        session.close()


# Obtener todos los usuarios (requiere token)
@login_bp.route("/usuarios", methods=["GET"])
@jwt_required()
def get_usuarios():
    identidad = get_jwt_identity()  # Datos guardados en el token

    session = SessionLocal()
    try:
        usuarios = session.query(User).all()
        return jsonify({
            "usuario_actual": identidad,  # Muestra quién hizo la consulta
            "usuarios": [
                {
                    "id": str(u.id),
                    "nom_usuario": u.nom_usuario,
                    "login": u.login,
                    "estado": u.estado,
                    "fec_creacion": u.fec_creacion.isoformat() if u.fec_creacion else None,
                    "fec_ult_entrada": u.fec_ult_entrada.isoformat() if u.fec_ult_entrada else None
                }
                for u in usuarios
            ]
        })
    finally:
        session.close()