from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..database import get_session
from ..models import Mazmorra, Enemigo
from ..schemas import MazmorraOut

router = APIRouter(prefix="/mazmorras", tags=["mazmorras"])

@router.get("", response_model=list[MazmorraOut])
async def list_mazmorras(session: AsyncSession = Depends(get_session)):
    res = await session.execute(select(Mazmorra).order_by(Mazmorra.orden))
    maz = res.scalars().unique().all()
    # carga explícita de enemigos (puedes usar selectinload si prefieres)
    for m in maz:
        await session.refresh(m, attribute_names=["enemigos"])
    return maz
