from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from city.models import City
from city.schemas import CityResponse, CityCreate
from city.crud import (
    get_cities as crud_get_cities,
    create_city as crud_create_city,
    get_city as crud_get_city,
    delete_city as crud_delete_city
)
from db.engine import SessionLocal

router = APIRouter()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


@router.get("/", response_model=list[CityResponse])
def get_cities(db: Session = Depends(get_db)) -> list[City]:
    return crud_get_cities(db)


@router.post("/", response_model=CityResponse)
def create_city(
        city: CityCreate,
        db: Session = Depends(get_db)
) -> City:
    return crud_create_city(db, city)


@router.get("/{city_id}", response_model=CityResponse)
def read_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> City:
    return crud_get_city(db, city_id)


@router.delete("/{city_id}")
def delete_city(
        city_id: int,
        db: Session = Depends(get_db)
) -> None | dict:
    return crud_delete_city(db, city_id)

