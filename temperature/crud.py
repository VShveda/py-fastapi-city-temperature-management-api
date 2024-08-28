import aiohttp
from sqlalchemy.orm import Session
from fastapi import HTTPException

from temperature.models import Temperature
from city.models import City


async def update_temperatures(db: Session, open_weather_map_key: str) -> None:
    cities = db.query(City).all()
    async with aiohttp.ClientSession() as session:
        for city in cities:
            async with session.get(
                    f"https://api.openweathermap.org/data/2.5/weather"
                    f"?q={city.name}"
                    f"&appid={open_weather_map_key}"
                    f"&units=metric"
            ) as response:
                if response.status == 200:
                    data = await response.json()
                    temperature = Temperature(
                        temperature=data["main"]["temp"],
                        city_id=city.id
                    )
                    db.add(temperature)
                    db.commit()


def get_temperatures(db: Session) -> list[Temperature]:
    return db.query(Temperature).all()


def get_temperature_by_city_id(db: Session, city_id: int) -> list[Temperature]:
    temperatures = (
        db.query(Temperature)
        .filter(Temperature.city_id == city_id)
        .all()
    )
    if not temperatures:
        raise HTTPException(status_code=404, detail="Temperature not found")
    return temperatures
