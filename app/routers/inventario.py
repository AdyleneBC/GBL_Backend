from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_session
from ..models import Inventario, Pocion
from ..schemas import InventarioItemOut, InventarioUpdate
from ..deps import get_current_user

router = APIRouter(prefix="/inventario", tags=["inventario"])

@router.get("", response_model=list[InventarioItemOut])
async def list_inventory(user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Inventario).where(Inventario.jugador_id == user.jugador_id))
    return res.scalars().all()

@router.post("/ajustar", response_model=InventarioItemOut)
async def adjust_inventory(payload: InventarioUpdate, user=Depends(get_current_user), session: AsyncSession = Depends(get_session)):
    # validar poción
    if not await session.get(Pocion, payload.pocion_id):
        raise HTTPException(404, "Poción no existe")
    res = await session.execute(
        select(Inventario).where(
            Inventario.jugador_id == user.jugador_id, Inventario.pocion_id == payload.pocion_id
        )
    )
    item = res.scalar_one_or_none()
    if not item:
        if payload.delta < 0:
            raise HTTPException(400, "No hay cantidad suficiente")
        item = Inventario(jugador_id=user.jugador_id, pocion_id=payload.pocion_id, cantidad=payload.delta)
        session.add(item)
    else:
        nueva = item.cantidad + payload.delta
        if nueva < 0:
            raise HTTPException(400, "No hay cantidad suficiente")
        item.cantidad = nueva
    await session.commit()
    await session.refresh(item)
    return item
