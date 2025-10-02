from flask_restx import Namespace, Resource, fields
from flask import request
from db import SessionLocal
from datetime import datetime, timedelta
from pytz import timezone
from models import User
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity, get_jwt

login_ns = Namespace("login", description="Operaciones de autenticación")
usuarios_ns = Namespace("usuarios", description="Gestión de usuarios")

login_model = login_ns.model("LoginRequest", {
    "login": fields.String(required=True, description="Usuario de acceso"),
    "password": fields.String(required=True, description="Contraseña")
})

login_response = login_ns.model("LoginResponse", {
    "message": fields.String(description="Mensaje de éxito"),
    "token": fields.String(description="JWT generado"),
    "usuario": fields.Nested(login_ns.model("UsuarioLogin", {
        "id": fields.String(description="ID del usuario"),
        "nom_usuario": fields.String(description="Nombre del usuario"),
        "login": fields.String(description="Usuario de acceso"),
        "fec_ult_entrada": fields.String(description="Última entrada (YYYY-MM-DD HH:MM:SS)")
    }))
})

usuario_model = usuarios_ns.model("Usuario", {
    "id": fields.String(description="ID del usuario"),
    "nom_usuario": fields.String(description="Nombre del usuario"),
    "login": fields.String(description="Usuario de acceso"),
    "estado": fields.String(description="Estado del usuario"),
    "fec_creacion": fields.String(description="Fecha de creación (ISO 8601)"),
    "fec_ult_entrada": fields.String(description="Última entrada (ISO 8601)")
})

usuarios_response = usuarios_ns.model("UsuariosResponse", {
    "usuario_actual": fields.Raw(description="Identidad obtenida del token JWT"),
    "usuarios": fields.List(fields.Nested(usuario_model))
})

@login_ns.route("")
class Login(Resource):
    @login_ns.expect(login_model)
    @login_ns.response(200, "Login exitoso", login_response)
    @login_ns.response(400, "Usuario y contraseña requeridos")
    @login_ns.response(401, "Credenciales inválidas")
    def post(self):
        """Inicia sesión y devuelve un token JWT"""
        data = request.get_json()
        login_user = data.get("login")
        password_user = data.get("password")

        if not login_user or not password_user:
            return {"error": "Usuario y contraseña requeridos"}, 400

        session = SessionLocal()
        try:
            user = session.query(User).filter(
                User.login == login_user,
                User.password == password_user
            ).first()

            if not user:
                return {"error": "Credenciales inválidas"}, 401

            # Actualizar fecha de última entrada
            now_colombia = datetime.now(timezone("America/Bogota")) + timedelta(hours=1)
            user.fec_ult_entrada = now_colombia
            session.commit()

            access_token = create_access_token(
                identity=str(user.id),
                additional_claims={"login": user.login},
                expires_delta=timedelta(hours=24)
            )

            return {
                "message": "Login exitoso",
                "token": access_token,
                "usuario": {
                    "id": str(user.id),
                    "nom_usuario": user.nom_usuario,
                    "login": user.login,
                    "fec_ult_entrada": now_colombia.strftime("%Y-%m-%d %H:%M:%S")
                }
            }, 200
        finally:
            session.close()


@usuarios_ns.route("")
class Usuarios(Resource):
    @usuarios_ns.response(200, "Lista de usuarios", usuarios_response)
    @jwt_required()
    def get(self):
        """Obtiene todos los usuarios (requiere token JWT)"""
        identidad = get_jwt_identity() 
        claims = get_jwt() 

        session = SessionLocal()
        try:
            usuarios = session.query(User).all()
            return {
                "usuario_actual": {
                    "id": identidad,
                    "login": claims.get("login")
                },
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
            }, 200
        finally:
            session.close()