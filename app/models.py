from sqlalchemy import String, Integer, Text, Boolean, TIMESTAMP, ForeignKey, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from .database import Base

class Jugador(Base):
    __tablename__ = "jugadores"
    jugador_id: Mapped[int] = mapped_column(primary_key=True)
    username: Mapped[str] = mapped_column(String(50), unique=True, nullable=False)
    email: Mapped[str] = mapped_column(String(120), unique=True, nullable=False)
    password_hash: Mapped[str] = mapped_column(String(255), nullable=False)
    fecha_registro: Mapped[str] = mapped_column(TIMESTAMP(timezone=True))

    inventario: Mapped[list["Inventario"]] = relationship(back_populates="jugador", cascade="all, delete-orphan")
    progresos: Mapped[list["Progreso"]] = relationship(back_populates="jugador", cascade="all, delete-orphan")

class Pocion(Base):
    __tablename__ = "pociones"
    pocion_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    tipo: Mapped[str | None] = mapped_column(String(40))
    descripcion: Mapped[str | None] = mapped_column(Text)
    efecto: Mapped[str | None] = mapped_column(String(80))

    inventario_items: Mapped[list["Inventario"]] = relationship(back_populates="pocion")

class Mazmorra(Base):
    __tablename__ = "mazmorras"
    mazmorra_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    tipo_medalla: Mapped[int | None] = mapped_column(Integer)
    dificultad: Mapped[int | None] = mapped_column(Integer)
    orden: Mapped[int] = mapped_column(Integer, nullable=False, unique=True)

    enemigos: Mapped[list["Enemigo"]] = relationship(back_populates="mazmorra", cascade="all, delete-orphan")
    progresos: Mapped[list["Progreso"]] = relationship(back_populates="mazmorra")

class Enemigo(Base):
    __tablename__ = "enemigos"
    enemigo_id: Mapped[int] = mapped_column(primary_key=True)
    nombre: Mapped[str] = mapped_column(String(80), nullable=False)
    descripcion: Mapped[str | None] = mapped_column(Text)
    poder: Mapped[int | None] = mapped_column(Integer)
    mazmorra_id: Mapped[int] = mapped_column(ForeignKey("mazmorras.mazmorra_id", ondelete="CASCADE"), nullable=False)

    mazmorra: Mapped[Mazmorra] = relationship(back_populates="enemigos")

class Progreso(Base):
    __tablename__ = "progreso"
    __table_args__ = (UniqueConstraint("jugador_id", "mazmorra_id", name="uq_jugador_mazmorra"),)
    progreso_id: Mapped[int] = mapped_column(primary_key=True)
    jugador_id: Mapped[int] = mapped_column(ForeignKey("jugadores.jugador_id", ondelete="CASCADE"), nullable=False)
    mazmorra_id: Mapped[int] = mapped_column(ForeignKey("mazmorras.mazmorra_id", ondelete="CASCADE"), nullable=False)
    medalla_id: Mapped[int | None] = mapped_column(Integer)
    completada: Mapped[bool] = mapped_column(Boolean, default=False, nullable=False)
    fecha_inicio: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))
    fecha_fin: Mapped[str | None] = mapped_column(TIMESTAMP(timezone=True))

    jugador: Mapped[Jugador] = relationship(back_populates="progresos")
    mazmorra: Mapped[Mazmorra] = relationship(back_populates="progresos")

class Inventario(Base):
    __tablename__ = "inventario"
    __table_args__ = (UniqueConstraint("jugador_id", "pocion_id", name="uq_inv_jugador_pocion"),)
    inventario_id: Mapped[int] = mapped_column(primary_key=True)
    jugador_id: Mapped[int] = mapped_column(ForeignKey("jugadores.jugador_id", ondelete="CASCADE"), nullable=False)
    pocion_id: Mapped[int] = mapped_column(ForeignKey("pociones.pocion_id", ondelete="CASCADE"), nullable=False)
    cantidad: Mapped[int] = mapped_column(Integer, nullable=False)

    jugador: Mapped[Jugador] = relationship(back_populates="inventario")
    pocion: Mapped[Pocion] = relationship(back_populates="inventario_items")
