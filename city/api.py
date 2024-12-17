from ninja import Router
from .models import City
from state.models import State
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from ninja_jwt.authentication import JWTAuth
from .schemas import CityIn, CityOut, CityUpdate


router = Router()


def city_exception(e):
    if type(e) == City.DoesNotExist:
        return 404, {"message": "Cidade não encontrada."}
    if type(e) == State.DoesNotExist:
        return 404, {"message": "Estado não encontrado."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=JWTAuth(), response={200: CityOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["City"], )
def save_city(request, payload: CityIn):
    try:
        state = State.objects.get(id=payload.state_id)
        city = City.objects.create(**payload.dict())
        city.state = state
        city.save()
        
        
        return city
    except (Exception, State.DoesNotExist) as e:
        return city_exception(e)



@router.get("/", auth=JWTAuth(),  response={200: List[CityOut], 404: MessageSchema}, tags=["City"],)
@paginate(LimitOffsetPagination)
def search_city(request, name=''):
    '''
    Lista as cidades.
    '''
    try:
        
        if name:
            citys = City.objects.filter(name__icontains=name)
        else:
            citys = City.objects.all()

        return citys
    except (Exception) as e:
        print(e)
        return []
    
@router.get("/by-state/{state_id}/", auth=JWTAuth(),  response={200: List[CityOut], 404: MessageSchema}, tags=["City"],)
@paginate(LimitOffsetPagination)
def search_city_by_state(request, state_id: int, name=''):
    '''
    Lista as cidades.
    '''
    try:
        state = State.objects.get(id=state_id)
        citys = City.objects.filter(state_id=state.id)
        if name:
            citys = City.objects.filter(name__icontains=name)
        return citys
    except (Exception, State.DoesNotExist) as e:
        return []
    


@router.get("/{city_id}/", response={200: CityOut, 404: MessageSchema, 500: MessageSchema}, tags=["City"], )
def detail_city(request, city_id: int):
    '''
    Recupera uma cidade pelo ID.
    '''

    try:
        city = City.objects.get(id=city_id)
        return city
    except (Exception, City.DoesNotExist) as e:
        return city_exception(e)


@router.put("/{city_id}/", response={200: CityOut, 404: MessageSchema, 500: MessageSchema}, tags=["City"], )
def update_city(request, payload: CityUpdate, city_id: int, ):
    '''
    Atualiza uma cidade pelo ID.
    '''

    try:
        city = City.objects.get(id=city_id)

        if payload.name:
            city.name = payload.name
        if payload.latitude:
            city.latitude = str(payload.latitude)
        if payload.longitude:
            city.longitude = str(payload.longitude)

        city.save()

        return city
    except (Exception, City.DoesNotExist) as e:
        return city_exception(e)

@router.delete("/{city_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["City"], )
def delete_city(request, city_id: int, ):
    '''
    Deleta uma cidade pelo ID.
    '''

    try:
        city = City.objects.get(id=city_id)
        city.delete()
        return 200, {"message": "Cidade deletada com sucesso."}
        
    except (Exception, State.DoesNotExist) as e:
        return city_exception(e)
