import enum
from sqlalchemy import (
    Column,
    Integer,
    String,
    Date,
    Time,
    Text,
    ForeignKey,
    Table,
    Enum,
)
from sqlalchemy.orm import relationship
from app.db.config import Base


class NivelPrueba(enum.Enum):
    BAJO = "Bajo"
    MODERADO = "Moderado"
    ALTO = "Alto"
    SEVERO = "Severo"


class TipoEvaluacion(enum.Enum):
    INICIAL = "Inicial"
    SEGUIMIENTO = "Seguimiento"
    EGRESO = "Egreso"


class TipoSesion(enum.Enum):
    INDIVIDUAL = "Individual"
    PAREJA = "Pareja"
    FAMILIAR = "Familiar"
    GRUPAL = "Grupal"


usuario_familia = Table(
    "usuario_familia",
    Base.metadata,
    Column("usuario_CURP", String(18), ForeignKey("usuario.CURP"), primary_key=True),
    Column("familia_id", Integer, ForeignKey("familia.id"), primary_key=True),
)


class Status(Base):
    __tablename__ = "status"
    id = Column(Integer, primary_key=True, index=True)
    estado = Column(String(50), unique=True, nullable=False)
    citas = relationship("Citas", back_populates="status")
    metas = relationship("Metas", back_populates="status")


class Psicologo(Base):
    __tablename__ = "psicologo"
    RFC = Column(String(13), primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(255), unique=True, nullable=True)
    especialidad = Column(String(255), nullable=True)
    cedula_profesional = Column(String(50), unique=True, nullable=False)
    citas = relationship("Citas", back_populates="psicologo")
    pruebas = relationship("Pruebas", back_populates="psicologo")
    evaluaciones = relationship("Evaluaciones", back_populates="psicologo")
    planes_tratamiento = relationship("PlanTratamiento", back_populates="psicologo")


class Usuario(Base):
    __tablename__ = "usuario"
    CURP = Column(String(18), primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    fecha_nacimiento = Column(Date)
    motivo = Column(Text, nullable=True)
    profesion = Column(String(255), nullable=True)
    domicilio = Column(Text, nullable=True)
    telefono = Column(String(15), nullable=True)
    correo = Column(String(255), unique=True, nullable=True)
    alergias = Column(Text, nullable=True)
    medicamento = Column(Text, nullable=True)
    familiares = relationship(
        "Familia", secondary=usuario_familia, back_populates="usuarios"
    )
    citas = relationship("Citas", back_populates="paciente")
    metas = relationship("Metas", back_populates="paciente")
    pruebas = relationship("Pruebas", back_populates="paciente")
    antecedentes = relationship("Antecedentes", back_populates="paciente")
    evaluaciones = relationship("Evaluaciones", back_populates="paciente")
    planes_tratamiento = relationship("PlanTratamiento", back_populates="paciente")


class Familia(Base):
    __tablename__ = "familia"
    id = Column(Integer, primary_key=True, index=True)
    nombre = Column(String(255), nullable=False)
    parentesco = Column(String(50), nullable=False)
    telefono = Column(String(15), nullable=True)
    usuarios = relationship(
        "Usuario", secondary=usuario_familia, back_populates="familiares"
    )


class Citas(Base):
    __tablename__ = "citas"
    id = Column(Integer, primary_key=True, index=True)
    psicologo_RFC = Column(String(13), ForeignKey("psicologo.RFC"), nullable=False)
    paciente_CURP = Column(String(18), ForeignKey("usuario.CURP"), nullable=False)
    fecha = Column(Date, nullable=False)
    hora = Column(Time, nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    notas = Column(Text, nullable=True)
    psicologo = relationship("Psicologo", back_populates="citas")
    paciente = relationship("Usuario", back_populates="citas")
    status = relationship("Status", back_populates="citas")
    sesion = relationship("Sesiones", back_populates="cita", uselist=False)


class Metas(Base):
    __tablename__ = "metas"
    id = Column(Integer, primary_key=True, index=True)
    paciente_CURP = Column(String(18), ForeignKey("usuario.CURP"), nullable=False)
    descripcion = Column(Text, nullable=False)
    status_id = Column(Integer, ForeignKey("status.id"), nullable=False)
    fecha_inicio = Column(Date, nullable=True)
    fecha_termino = Column(Date, nullable=True)
    notas = Column(Text, nullable=True)
    paciente = relationship("Usuario", back_populates="metas")
    status = relationship("Status", back_populates="metas")


class Pruebas(Base):
    __tablename__ = "pruebas"
    id = Column(Integer, primary_key=True, index=True)
    psicologo_RFC = Column(String(13), ForeignKey("psicologo.RFC"), nullable=False)
    paciente_CURP = Column(String(18), ForeignKey("usuario.CURP"), nullable=False)
    tipo_prueba = Column(String(255), nullable=False)
    resultado = Column(Text, nullable=True)
    puntaje = Column(Integer, nullable=True)
    nivel = Column(Enum(NivelPrueba), nullable=True)
    archivo_adjunto = Column(String(255), nullable=True)
    notas = Column(Text, nullable=True)
    psicologo = relationship("Psicologo", back_populates="pruebas")
    paciente = relationship("Usuario", back_populates="pruebas")


class Antecedentes(Base):
    __tablename__ = "antecedentes"
    id = Column(Integer, primary_key=True, index=True)
    paciente_CURP = Column(
        String(18), ForeignKey("usuario.CURP"), unique=True, nullable=False
    )
    antecedentes_familiares = Column(Text, nullable=True)
    antecedentes_personales = Column(Text, nullable=True)
    antecedentes_medicos = Column(Text, nullable=True)
    antecedentes_psicologicos = Column(Text, nullable=True)
    paciente = relationship("Usuario", back_populates="antecedentes", uselist=False)


class Evaluaciones(Base):
    __tablename__ = "evaluaciones"
    id = Column(Integer, primary_key=True, index=True)
    paciente_CURP = Column(String(18), ForeignKey("usuario.CURP"), nullable=False)
    psicologo_RFC = Column(String(13), ForeignKey("psicologo.RFC"), nullable=False)
    tipo_evaluacion = Column(Enum(TipoEvaluacion), nullable=False)
    fecha = Column(Date, nullable=False)
    observaciones = Column(Text, nullable=True)
    diagnostico = Column(Text, nullable=True)
    recomendaciones = Column(Text, nullable=True)
    paciente = relationship("Usuario", back_populates="evaluaciones")
    psicologo = relationship("Psicologo", back_populates="evaluaciones")


class PlanTratamiento(Base):
    __tablename__ = "plan_tratamiento"
    id = Column(Integer, primary_key=True, index=True)
    paciente_CURP = Column(String(18), ForeignKey("usuario.CURP"), nullable=False)
    psicologo_RFC = Column(String(13), ForeignKey("psicologo.RFC"), nullable=False)
    objetivos = Column(Text, nullable=False)
    tecnicas = Column(Text, nullable=False)
    frecuencia = Column(String(255), nullable=True)
    duracion_estimda = Column(String(255), nullable=True)
    fecha_inicio = Column(Date, nullable=False)
    fecha_revision = Column(Date, nullable=True)
    paciente = relationship("Usuario", back_populates="planes_tratamiento")
    psicologo = relationship("Psicologo", back_populates="planes_tratamiento")


class Sesiones(Base):
    __tablename__ = "sesiones"
    id = Column(Integer, primary_key=True, index=True)
    cita_id = Column(Integer, ForeignKey("citas.id"), unique=True, nullable=False)
    tipo_sesion = Column(Enum(TipoSesion), nullable=False)
    tema = Column(String(255), nullable=True)
    observaciones = Column(Text, nullable=True)
    avances = Column(Text, nullable=True)
    tareas = Column(Text, nullable=True)
    cita = relationship("Citas", back_populates="sesion")