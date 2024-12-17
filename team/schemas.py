from ninja import ModelSchema, Schema
from .models import Team
from typing import Optional
from town_hall.schemas import TownHallOut


class TeamOut(ModelSchema):
    town_hall: TownHallOut
    class Config:
        model = Team
        model_fields = ['id', 'name',]

class TeamIn(ModelSchema):
    town_hall_id: int
    class Config:
        model = Team
        model_exclude = ['id', 'town_hall']

class TeamUpdate(Schema):
    name: Optional[str] = None
    town_hall_id: Optional[int] = None