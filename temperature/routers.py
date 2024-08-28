import os

from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from dotenv import load_dotenv

from temperature.models import Temperature
from temperature.schemas import TemperatureResponse
from temperature.crud import (
    get_temperatures as crud_get_temperatures,
    update_temperatures as crud_update_temperatures,
    get_temperature_by_city_id as crud_get_temperature_by_city_id
)
from db.engine import SessionLocal

load_dotenv()

OPEN_WEATHER_MAP_KEY = os.getenv("OPEN_WEATHER_MAP_KEY")

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[TemperatureResponse])
def get_temperatures(db: Session = Depends(get_db)) -> list[Temperature]:
    return crud_get_temperatures(db)


@router.post("/update")
async def update_temperatures(db: Session = Depends(get_db)) -> None:
    await crud_update_temperatures(db, OPEN_WEATHER_MAP_KEY)


@router.get("/{city_id}", response_model=list[TemperatureResponse])
def get_temperature_by_city_id(
        city_id: int,
        db: Session = Depends(get_db)
) -> list[Temperature]:
    return crud_get_temperature_by_city_id(db, city_id)
