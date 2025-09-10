from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, update, insert
from datetime import datetime, timezone
from ..database import get_session
from ..models import Progreso, Mazmorra
from ..schemas import ProgresoOut
from ..deps import get_current_user

router = APIRouter(prefix="/progreso", tags=["progreso"])

@router.get("", response_model=list[ProgresoOut])
async def my_progress(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Progreso).where(Progreso.jugador_id == user.jugador_id))
    return res.scalars().all()

@router.post("/{mazmorra_id}/start", response_model=ProgresoOut)
async def start_dungeon(mazmorra_id: int, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # validar que existe la mazmorra
    m = await session.get(Mazmorra, mazmorra_id)
    if not m:
        raise HTTPException(404, "Mazmorra no existe")
    now = datetime.now(timezone.utc)
    # UPSERT manual
    res = await session.execute(select(Progreso).where(Progreso.jugador_id==user.jugador_id, Progreso.mazmorra_id==mazmorra_id))
    p = res.scalar_one_or_none()
    if p:
        p.completada = False
        p.fecha_inicio = now
        p.fecha_fin = None
    else:
        p = Progreso(jugador_id=user.jugador_id, mazmorra_id=mazmorra_id, fecha_inicio=now, completada=False)
        session.add(p)
    await session.commit()
    await session.refresh(p)
    return p

@router.post("/{mazmorra_id}/complete", response_model=ProgresoOut)
async def complete_dungeon(mazmorra_id: int, medalla_id: int | None = None, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Progreso).where(Progreso.jugador_id==user.jugador_id, Progreso.mazmorra_id==mazmorra_id))
    p = res.scalar_one_or_none()
    if not p:
        raise HTTPException(400, "Debes iniciar la mazmorra primero")
    p.completada = True
    p.medalla_id = medalla_id
    from datetime import datetime, timezone
    p.fecha_fin = datetime.now(timezone.utc)
    await session.commit()
    await session.refresh(p)
    return p
