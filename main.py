from __future__ import annotations

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.api.routes import app_version, announcements, configs, countries, health, networks
from app.config.settings import get_settings
from app.database.session import init_db

settings = get_settings()

app = FastAPI(
    title=settings.app_name,
    version='1.0.0',
    description='VUKA backend for VPN config management.',
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

app.include_router(health.router)
app.include_router(configs.router)
app.include_router(countries.router)
app.include_router(networks.router)
app.include_router(announcements.router)
app.include_router(app_version.router)


@app.on_event('startup')
async def on_startup() -> None:
    await init_db()


@app.get('/')
async def root() -> dict[str, str]:
    return {'message': 'VUKA backend is running.'}
