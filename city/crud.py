from sqlalchemy.orm import Session
from sqlalchemy.exc import NoResultFound
from fastapi import HTTPException

from city.models import City
from city.schemas import CityCreate


def get_cities(db: Session) -> list[City]:
    return db.query(City).all()


def create_city(db: Session, city: CityCreate) -> City:
    db_city = City(name=city.name, additional_info=city.additional_info)
    db.add(db_city)
    db.commit()
    db.refresh(db_city)
    return db_city


def get_city(db: Session, city_id: int) -> City:
    try:
        return db.query(City).filter(City.id == city_id).one()
    except NoResultFound:
        raise HTTPException(status_code=404, detail="City not found")


def delete_city(db: Session, city_id: int) -> dict:
    city = db.query(City).filter(City.id == city_id).first()
    if not city:
        raise HTTPException(status_code=404, detail="City not found")
    db.delete(city)
    db.commit()
    return {"message": "City deleted"}
