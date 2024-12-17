from ninja import Router
from .models import Daily, ImagesDaily
from my_auth.models import UserMobile
from problem.models import Problem
from city.models import City
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from .schemas import DailyIn, DailyOut, DailyUpdate
from manubrasil_backend.util.util_functions import convert_image_base64_to_file
from dotenv import load_dotenv
from ninja.security import HttpBasicAuth
import os

router = Router()


load_dotenv()

SECRET_AUTH_REQ = os.getenv('SECRET_AUTH_REQ')
SECRET_PASSWORD_REQ = os.getenv('SECRET_PASSWORD_REQ')


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        if username == SECRET_AUTH_REQ and password == SECRET_PASSWORD_REQ:
            return username


def daily_exception(e):
    if type(e) == Daily.DoesNotExist:
        return 404, {"message": "Diário não encontrado."}
    if type(e) == UserMobile.DoesNotExist:
        return 404, {"message": "Usuário não encontrado."}
    if type(e) == Problem.DoesNotExist:
        return 404, {"message": "Problema não encontrado."}
    if type(e) == City.DoesNotExist:
        return 404, {"message": "Município não encontrado."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=BasicAuth(), response={200: DailyOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Daily"], )
def save_daily(request, payload: DailyIn):
    try:
        user = UserMobile.objects.get(id=payload.user_id)
        problem = Problem.objects.get(id=payload.problem_id)
        toDict = payload.dict()
        images = payload.dict().pop("images")
        del toDict['images']
        daily = Daily.objects.create(**toDict)
        daily.user = user
        daily.problem = problem
        daily.save()

        if payload.images:
            i = 0

            for image in images:
                i += 1
                image_converted = convert_image_base64_to_file(
                    image['file'], 'image_daily' + str(daily.id) + "_" + str(i))
                imagedaily = ImagesDaily()
                imagedaily.file = image_converted
                imagedaily.daily = daily
                imagedaily.save()

        daily.images = daily.image_daily.all()

        return daily
    except (Exception) as e:
        return daily_exception(e)


@router.get("/", response=List[DailyOut], tags=["Daily"], auth=BasicAuth())
@paginate(LimitOffsetPagination)
def search_daily(request, city=''):
    '''
    Lista os chamados.
    '''

    if city:
        dailys = Daily.objects.filter(city__iexact=city)
    else:
        dailys = Daily.objects.all()

    for daily in dailys:
        daily.images = daily.image_daily.all()

    return dailys


@router.get("/by-user/{user_id}/", response=List[DailyOut], tags=["Daily"], auth=BasicAuth())
@paginate(LimitOffsetPagination)
def daily_by_user(request, user_id: int):
    '''
    Lista os diários por usuário.
    '''
    try:
        user = UserMobile.objects.get(id=user_id)
        dailys = Daily.objects.filter(user__id=user.id)
        for daily in dailys:
            daily.images = daily.image_daily.all()

        return dailys
    except (Exception, UserMobile.DoesNotExist) as e:
        print(e)
        return []


@router.get("/{daily_id}/", response={200: DailyOut, 404: MessageSchema, 500: MessageSchema}, tags=["Daily"], auth=BasicAuth())
def detail_daily(request, daily_id: int):
    '''
    Recupera um diário pelo ID.
    '''

    try:
        daily = Daily.objects.get(id=daily_id)
        daily.images = daily.image_daily.all()
        return daily
    except (Exception, Daily.DoesNotExist) as e:
        return daily_exception(e)


@router.put("/{daily_id}/", response={200: DailyOut, 404: MessageSchema, 500: MessageSchema}, tags=["Daily"], auth=BasicAuth())
def update_daily(request, payload: DailyUpdate, daily_id: int, ):
    '''
    Atualiza um diário pelo ID.
    '''

    try:
        daily = Daily.objects.get(id=daily_id)

        if payload.problem_id:
            problem = Problem.objects.get(id=payload.problem_id)
            daily.problem = problem
        if payload.additional_information:
            daily.additional_information = payload.additional_information
        if payload.city:
            daily.city = payload.city

        daily.save()

        if payload.images:
            i = 0
            ImagesDaily.objects.filter(daily__id=daily.id).delete()
            images = payload.dict().pop("images")
            for image in images:
                i += 1
                image_converted = convert_image_base64_to_file(
                    image['file'], 'image_daily' + str(daily.id) + "_" + str(i))
                imagedaily = ImagesDaily()
                imagedaily.file = image_converted
                imagedaily.daily = daily
                imagedaily.save()

        daily.images = daily.image_daily.all()
        return daily
    except (Exception, Daily.DoesNotExist, City.DoesNotExist, UserMobile.DoesNotExist, Problem.DoesNotExist) as e:
        return daily_exception(e)


@router.delete("/{daily_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Daily"], auth=BasicAuth())
def delete_daily(request, daily_id: int, ):
    '''
    Deleta um diário pelo ID.
    '''

    try:
        daily = Daily.objects.get(id=daily_id)
        daily.delete()
        return 200, {"message": "Diário deletado com sucesso."}

    except (Exception, Daily.DoesNotExist) as e:
        return daily_exception(e)
