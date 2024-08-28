from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None


class CityResponse(BaseModel):
    id: int
    name: str
    additional_info: str | None = None

    class Config:
        from_attributes = True
