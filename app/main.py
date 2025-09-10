from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from .database import engine, Base
from .routers import auth as auth_router, mazmorras as maz_router, progreso as prog_router, inventario as inv_router

app = FastAPI(title="Game SQL API")

# CORS: ajusta origins con tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # pon aquí tu dominio del front en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# crear tablas automáticamente (para prototipos). En producción usa Alembic.
@app.on_event("startup")
async def on_startup():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app.include_router(auth_router.router)
app.include_router(maz_router.router)
app.include_router(prog_router.router)
app.include_router(inv_router.router)
