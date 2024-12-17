from ninja import ModelSchema, Schema
from typing import Optional
from .models import User, Team, TownHall, UserMobile
from city.models import City
from state.models import State

class StateOutCity(ModelSchema):
    class Config:
        model = State
        model_fields = ['id', 'name']


class CityOutUser(ModelSchema):
    state: StateOutCity
    class Config:
        model = City
        model_fields = ['id', 'name',
                        'latitude', 'longitude']


class TownHallOut(ModelSchema):
    class Config:
        model = TownHall
        model_fields = ['id', 'name',
                        'address', 'infos', 'generates_open_os']


class TeamOut(ModelSchema):
    town_hall: TownHallOut

    class Config:
        model = Team
        model_fields = ['id', 'name']


class UserOutSchema(ModelSchema):
    team: Optional[TeamOut] = None
    city: Optional[CityOutUser] = None
    town_hall: Optional[TownHallOut] = None

    class Config:
        model = User
        model_fields = ['id', 'email', 'name', 'username',
                        'type', 'team', 'city', 'town_hall', 'photo', ]


class UserMobileOut(ModelSchema):
    class Config:
        model = UserMobile
        model_fields = ['id', 'email', 'full_name', 'cpf',
                        'number_phone', 'type', 'password']


class UserMobileRecoverPassword(Schema):
    code: int
    email: str


class UserSendEmailRecoverPassword(ModelSchema):
    class Config:
        model = User
        model_fields = ['email']


class UserSendEmailRecoverPasswordMobile(Schema):
    email: str


class UserRecoverPassword(Schema):
    token: str
    password: str
    confirm_password: str


class UserUpdatePassword(Schema):
    password: str
    confirm_password: str

class UserAuthenticate(ModelSchema):
    class Config:
        model = User
        model_fields = ['username', 'password']

class UserMobileAuthenticate(ModelSchema):
    class Config:
        model = User
        model_fields = ['email', 'password']

class UserIn(ModelSchema):
    team: int
    city: int
    town_hall: int
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    photo: Optional[str] = None

    class Config:
        model = User
        model_fields = ['name', 'email', 'password', 'type']

class UserUpdateSchema(Schema):
    team: Optional[int] = None
    city: Optional[int] = None
    town_hall: Optional[int] = None
    password: Optional[str] = None
    confirm_password: Optional[str] = None
    name: Optional[str] = None
    email: Optional[str] = None
    type: Optional[str] = None
    photo: Optional[str] = None

class UserMobileIn(ModelSchema):
    
    class Config:
        model = UserMobile
        model_fields = ['email', 'full_name', 'cpf',
                        'password', 'number_phone', 'type']

class UserMobileUpdatePassword(Schema):
    user_id: int
    new_password: str
    confirm_new_password: str

class UserMobileUpdateSchema(Schema):
    email: Optional[str] = None
    full_name: Optional[str] = None
    cpf: Optional[str] = None
    number_phone: Optional[str] = None
    type: Optional[str] = None