from ninja import ModelSchema, Schema
from .models import Problem
from typing import Optional


class ProblemOut(ModelSchema):
    class Config:
        model = Problem
        model_fields = ['id', 'description', 'type']

class ProblemIn(ModelSchema):
    class Config:
        model = Problem
        model_exclude = ['id']

class ProblemUpdate(Schema):
    description: Optional[str] = None
    type: Optional[str] = None
