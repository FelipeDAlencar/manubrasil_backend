from ninja import ModelSchema, Schema
from .models import Daily, ImagesDaily
from typing import Optional, List
from my_auth.models import UserMobile
from problem.schemas import ProblemOut

class ImageIn(ModelSchema):
    class Config:
        model = ImagesDaily
        model_exclude = ['id', 'daily',]

class ImageOut(ModelSchema):
    class Config:
        model = ImagesDaily
        model_fields = ['id', 'file']

class UserMobileOutDaily(ModelSchema):
    class Config:
        model = UserMobile
        model_fields = ['id', 'email', 'full_name', 'cpf',
                        'type',]


class DailyOut(ModelSchema):
    problem: ProblemOut
    user: UserMobileOutDaily
    images: Optional[List[ImageOut]] = []
    class Config:
        model = Daily
        model_fields = ['id', 'additional_information', 'city', 'date']

class DailyIn(ModelSchema):
    problem_id: int
    user_id: int
    images: Optional[List[ImageIn]] = None
    class Config:
        model = Daily
        model_exclude = ['id', 'user', 'problem']

class DailyUpdate(Schema):
    problem_id: Optional[int] = None
    images: Optional[List[ImageIn]] = None
    city: Optional[str] = None
    additional_information: Optional[str] = None

    