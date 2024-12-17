from ninja import ModelSchema, Schema
from .models import ServiceOrder
from called.schemas import CalledOut
from typing import Optional, List

class ServiceOrderIn(ModelSchema):
    calleds_ids: Optional[List[int]] = None
    problem_id: Optional[int] = None
    city_id: Optional[int] = None
    localization:  Optional[str] = None
    lat: Optional[str] = None
    lng: Optional[str] = None
    #additional_information: Optional[str] = None
    
    class Config:
        model = ServiceOrder
        model_exclude = ['id', 'create_at', 'open_date']


class ServiceOrderOut(ModelSchema):
    calleds: Optional[List[CalledOut]] = []
    first_called: Optional[CalledOut] = None

    class Config:
        model = ServiceOrder
        model_fields = ['id', 'status',
                        'create_at', 'description', 'open_date']


class ServiceOrderUpdate(Schema):
    problem_id: Optional[int] = None
    city_id: Optional[int] = None
    status: Optional[str] = None
    description: Optional[str] = None
    localization: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None
    calleds_ids: Optional[List[int]] = None
