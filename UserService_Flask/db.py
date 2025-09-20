from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os

# Variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_SERVER = os.getenv("DB_SERVER")  # Ej: KENNETH\MSSQLSERVER01
DB_NAME = os.getenv("DB_NAME")

DATABASE_URL = (
    f"mssql+pyodbc://{DB_USER}:{DB_PASSWORD}@{DB_SERVER}/{DB_NAME}"
    "?driver=ODBC+Driver+17+for+SQL+Server&TrustServerCertificate=yes"
)

# Crear conexión
engine = create_engine(DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind=engine)