from ninja import ModelSchema, Schema
from .models import Called, ImagesCalled
from typing import Optional, List
from my_auth.models import UserMobile, User
from problem.schemas import ProblemOut
from city.schemas import CityOutRelation


class ImageIn(ModelSchema):
    class Config:
        model = ImagesCalled
        model_exclude = ['id', 'called', ]


class ImageOut(ModelSchema):
    class Config:
        model = ImagesCalled
        model_fields = ['id', 'file']


class UserMobileOutCalled(ModelSchema):
    class Config:
        model = UserMobile
        model_fields = ['id', 'email', 'full_name', 'cpf',

                        'type', ]


class UserOutCalled(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'email',
                        'type', ]


class CalledOut(ModelSchema):
    problem: ProblemOut
    user_mobile: Optional[UserMobileOutCalled] = None
    user: Optional[UserOutCalled] = None
    images: Optional[List[ImageOut]] = []
    city: Optional[CityOutRelation] = None

    class Config:
        model = Called
        model_fields = ['id', 'localization', 'lat', 'lng',
                        'status', 'additional_information', 'date', 'first_called']


class CalledIn(ModelSchema):
    problem_id: int
    city_id: int
    service_order_id: Optional[int] = None
    user_mobile_id: Optional[int] = None
    user_id: Optional[int] = None
    images: Optional[List[ImageIn]] = None

    class Config:
        model = Called
        model_exclude = ['id', 'user_mobile', 'user',
                         'problem', 'city', 'service_order', 'first_called', 'date']


class CalledUpdate(Schema):
    problem_id: Optional[int] = None
    user_id: Optional[int] = None
    user_mobile_id: Optional[int] = None
    city_id: Optional[int] = None
    status: Optional[str] = None
    lat: Optional[float] = None
    lng: Optional[float] = None
    localization: Optional[str] = None
    additional_information: Optional[str] = None
