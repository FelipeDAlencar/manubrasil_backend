from ninja import Router
from .models import Neighborhood
from city.models import City
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from ninja_jwt.authentication import JWTAuth
from .schemas import NeighborhoodIn, NeighborhoodOut, NeighborhoodUpdate


router = Router()


def neighborhood_exception(e):
    if type(e) == Neighborhood.DoesNotExist:
        return 404, {"message": "Bairro não encontrado."}
    if type(e) == City.DoesNotExist:
        return 404, {"message": "Município não encontrado."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=JWTAuth(), response={200: NeighborhoodOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Neighborhood"], )
def save_neighborhood(request, payload: NeighborhoodIn):
    try:
        city = City.objects.get(id=payload.city_id)
        neighborhood = Neighborhood.objects.create(**payload.dict())
        neighborhood.city = city
        neighborhood.save()
        return neighborhood
    except (Exception, City.DoesNotExist) as e:
        return neighborhood_exception(e)


@router.get("/by-city/{city_id}/", response=List[NeighborhoodOut], tags=["Neighborhood"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_neighborhood_by_city(request, city_id:int, name=''):
    '''
    Lista os bairros.
    '''
    try:
        city = City.objects.get(id=city_id)
        neighborhoods = Neighborhood.objects.filter(city_id=city.id)
        if name:
            neighborhoods = neighborhoods.filter(name__icontains=name)

        return neighborhoods
    except:
        return []


@router.get("/{neighborhood_id}/", response={200: NeighborhoodOut, 404: MessageSchema, 500: MessageSchema}, tags=["Neighborhood"], auth=JWTAuth())
def detail_neighborhood(request, neighborhood_id: int):
    '''
    Recupera um bairro pelo ID.
    '''

    try:
        neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        return neighborhood
    except (Exception, Neighborhood.DoesNotExist) as e:
        return neighborhood_exception(e)


@router.put("/{neighborhood_id}/", response={200: NeighborhoodOut, 404: MessageSchema, 500: MessageSchema}, tags=["Neighborhood"], auth=JWTAuth())
def update_neighborhood(request, payload: NeighborhoodUpdate, neighborhood_id: int, ):
    '''
    Atualiza um bairro pelo ID.
    '''

    try:
        neighborhood = Neighborhood.objects.get(id=neighborhood_id)

        if payload.name:
            neighborhood.name = payload.name

        neighborhood.save()

        return neighborhood
    except (Exception, Neighborhood.DoesNotExist) as e:
        return neighborhood_exception(e)


@router.delete("/{neighborhood_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Neighborhood"], auth=JWTAuth())
def delete_neighborhood(request, neighborhood_id: int, ):
    '''
    Deleta um bairro pelo ID.
    '''

    try:
        neighborhood = Neighborhood.objects.get(id=neighborhood_id)
        neighborhood.delete()
        return 200, {"message": "Bairro deletado com sucesso."}

    except (Exception, Neighborhood.DoesNotExist) as e:
        return neighborhood_exception(e)
