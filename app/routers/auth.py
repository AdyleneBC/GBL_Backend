from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_session
from ..models import Jugador
from ..schemas import UserCreate, UserOut, Token
from ..auth import hash_password, verify_password, create_access_token

router = APIRouter(prefix="/auth", tags=["auth"])

@router.post("/register", response_model=UserOut)
async def register(data: UserCreate, session: AsyncSession = Depends(get_session)):
    # username/email únicos (SQL injection-safe vía SQLAlchemy parametrizado)
    exists = await session.execute(select(Jugador).where((Jugador.username == data.username) | (Jugador.email == data.email)))
    if exists.scalar_one_or_none():
        raise HTTPException(status_code=409, detail="Usuario o email ya registrado")

    user = Jugador(username=data.username, email=data.email, password_hash=hash_password(data.password))
    session.add(user)
    await session.commit()
    await session.refresh(user)
    return user

@router.post("/login", response_model=Token)
async def login(data: UserCreate, session: AsyncSession = Depends(get_session)):
    q = await session.execute(select(Jugador).where(Jugador.username == data.username))
    user = q.scalar_one_or_none()
    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Credenciales inválidas")
    return {"access_token": create_access_token(sub=user.username), "token_type": "bearer"}
