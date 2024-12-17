from ninja import Router
from .models import TownHall
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from ninja_jwt.authentication import JWTAuth
from .schemas import TownHallIn, TownHallOut, TownHallUpdate


router = Router()


def town_all_exception(e):
    if type(e) == TownHall.DoesNotExist:
        return 404, {"message": "Prefeitura não encontrada."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=JWTAuth(), response={200: TownHallOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Town Hall"], )
def save_town_hall(request, payload: TownHallIn):
    try:
        town_hall = TownHall.objects.create(**payload.dict())
        town_hall.save()
        return town_hall
    except (Exception) as e:
        return town_all_exception(e)


@router.get("/", response=List[TownHallOut], tags=["Town Hall"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_town_hall(request, name=''):
    '''
    Lista as prefeituras.
    '''

    if name:
        town_halls = TownHall.objects.filter(name__icontains=name)
    else:
        town_halls = TownHall.objects.all()

    return town_halls


@router.get("/{town_hall_id}/", response={200: TownHallOut, 404: MessageSchema, 500: MessageSchema}, tags=["Town Hall"], auth=JWTAuth())
def detail_town_hall(request, town_hall_id: int):
    '''
    Recupera uma prefeitura pelo ID.
    '''

    try:
        town_hall = TownHall.objects.get(id=town_hall_id)
        return town_hall
    except (Exception, TownHall.DoesNotExist) as e:
        return town_all_exception(e)


@router.put("/{town_hall_id}/", response={200: TownHallOut, 404: MessageSchema, 500: MessageSchema}, tags=["Town Hall"], auth=JWTAuth())
def update_town_hall(request, payload: TownHallUpdate, town_hall_id: int, ):
    '''
    Atualiza uma prefeitura pelo ID.
    '''

    try:
        town_hall = TownHall.objects.get(id=town_hall_id)

        if payload.name:
            town_hall.name = payload.name
        if payload.address:
            town_hall.address = payload.address
        if payload.infos:
            town_hall.infos = payload.infos
        if payload.generates_open_os:
            town_hall.generates_open_os = payload.generates_open_os

        town_hall.save()

        return town_hall
    except (Exception, TownHall.DoesNotExist) as e:
        return town_all_exception(e)


@router.delete("/{town_hall_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Town Hall"], auth=JWTAuth())
def delete_town_hall(request, town_hall_id: int, ):
    '''
    Deleta uma prefeitura pelo ID.
    '''

    try:
        town_hall = TownHall.objects.get(id=town_hall_id)
        town_hall.delete()
        return 200, {"message": "Prefeitura deletada com sucesso."}

    except (Exception, TownHall.DoesNotExist) as e:
        print(e)
        return town_all_exception(e)
