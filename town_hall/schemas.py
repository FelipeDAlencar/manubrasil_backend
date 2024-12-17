from ninja import ModelSchema, Schema
from .models import TownHall
from typing import Optional
from city.schemas import CityOut


class TownHallOut(ModelSchema):
    class Config:
        model = TownHall
        model_fields = ['id', 'name', 'address', 'infos', 'generates_open_os']

class TownHallIn(ModelSchema):
    class Config:
        model = TownHall
        model_exclude = ['id',]

class TownHallUpdate(Schema):
    name: Optional[str] = None
    address: Optional[str] = None
    infos: Optional[str] = None
    generates_open_os: Optional[bool] = None
