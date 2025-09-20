from sqlalchemy import Column, String, Integer, DateTime
from sqlalchemy.dialects.mssql import UNIQUEIDENTIFIER
from sqlalchemy.orm import declarative_base
from datetime import datetime
import uuid

Base = declarative_base()

class User(Base):
    __tablename__ = "Tb_Usuario"  # Nombre exacto en la BD
    __table_args__ = {"schema": "Usuarios"} 

    id = Column(UNIQUEIDENTIFIER, primary_key=True, default=uuid.uuid4)
    nom_usuario = Column(String(200), nullable=False)
    cargo_id = Column(Integer, nullable=False)
    codigo = Column(Integer, nullable=False)
    login = Column(String(50), nullable=False, unique=True)
    password = Column(String(100), nullable=False)
    estado = Column(Integer, nullable=False)
    fec_creacion = Column(DateTime, default=datetime.utcnow, nullable=False)
    fec_ult_entrada = Column(DateTime, nullable=True)