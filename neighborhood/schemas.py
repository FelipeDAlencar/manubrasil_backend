from ninja import ModelSchema, Schema
from .models import Neighborhood
from typing import Optional
from city.schemas import CityOut


class NeighborhoodOut(ModelSchema):
    city: CityOut
    class Config:
        model = Neighborhood
        model_fields = ['id', 'name']

class NeighborhoodIn(ModelSchema):
    city_id: int
    class Config:
        model = Neighborhood
        model_exclude = ['id', 'city']

class NeighborhoodUpdate(Schema):
    name: Optional[str] = None