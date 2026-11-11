from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Boolean,
    ForeignKey
)

from sqlalchemy.orm import declarative_base


Base = declarative_base()


class Usuario(Base):

    __tablename__ = "usuarios"

    id = Column(
        Integer,
        primary_key=True
    )

    identificacion = Column(
        String(30),
        unique=True,
        nullable=False
    )

    nombre_completo = Column(
        String(300),
        nullable=False
    )

    correo = Column(
        String(250),
        unique=True
    )

    usuario = Column(
        String(100),
        unique=True,
        nullable=False
    )

    rol = Column(
        String(50),
        nullable=False
    )

    estado = Column(
        Boolean,
        default=True
    )


class Delito(Base):

    __tablename__ = "delitos"

    id = Column(
        Integer,
        primary_key=True
    )

    codigo = Column(
        String(20),
        unique=True,
        nullable=False
    )

    nombre = Column(
        String(300),
        nullable=False
    )

    pena_maxima_meses = Column(
        Integer,
        nullable=False
    )

    activo = Column(
        Boolean,
        default=True
    )

class Caso(Base):

    __tablename__ = "casos"

    id = Column(
        Integer,
        primary_key=True
    )

    radicado = Column(
        String(21),
        unique=True,
        nullable=False
    )

    fecha_hechos = Column(
        Date,
        nullable=False
    )

    delito_id = Column(
        Integer,
        nullable=False
    )

    pena_maxima_meses = Column(
        Integer,
        nullable=False
    )

    fecha_prescripcion = Column(
        Date,
        nullable=False
    )

    estado_caso = Column(
        String(20),
        nullable=False,
        default="ACTIVO"
    )  
class OrdenPJ(Base):

    __tablename__ = "ordenes_pj"

    id = Column(
        Integer,
        primary_key=True
    )

    caso_id = Column(
        Integer,
        ForeignKey("casos.id"),
        nullable=False
    )

    numero_orden = Column(
        String(50),
        unique=True,
        nullable=False
    )

    tipo_orden = Column(
        String(100),
        nullable=False
    )

    fecha_inicio = Column(
        Date,
        nullable=False
    )

    termino_dias = Column(
        Integer,
        nullable=False
    )

    fecha_vencimiento = Column(
        Date,
        nullable=False
    )

    estado = Column(
        String(30),
        nullable=False,
        default="PENDIENTE"
    )

    semaforo = Column(
        String(20),
        nullable=False,
        default="VERDE"
    )      