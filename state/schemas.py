from ninja import ModelSchema, Schema
from .models import State
from typing import Optional


class StateOut(ModelSchema):
    class Config:
        model = State
        model_fields = ['id', 'name']

class StateIn(ModelSchema):
    class Config:
        model = State
        model_fields = ['id','name']

class StateUpdate(Schema):
    name: Optional[str] = None