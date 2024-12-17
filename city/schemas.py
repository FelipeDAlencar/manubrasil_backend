from ninja import ModelSchema, Schema
from .models import City
from typing import Optional
from state.schemas import StateOut

class CityOutRelation(ModelSchema):
    class Config:
        model = City
        model_fields = ["id", "name"]


class CityOut(ModelSchema):
    state: StateOut
    class Config:
        model = City
        model_fields = ['id', 'name', 'latitude', 'longitude',]

class CityIn(ModelSchema):
    state_id: int
    class Config:
        model = City
        model_exclude = ['id', 'state']

class CityUpdate(Schema):
    name: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None