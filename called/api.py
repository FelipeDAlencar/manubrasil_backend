from ninja import Router
from .models import Called, ImagesCalled
from my_auth.models import UserMobile, User
from problem.models import Problem
from service_order.models import ServiceOrder
from city.models import City
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from .schemas import CalledIn, CalledOut, CalledUpdate
from manubrasil_backend.util.util_functions import convert_image_base64_to_file
from dotenv import load_dotenv
from ninja.security import HttpBasicAuth
import os
from django.db.models import Q

router = Router()


load_dotenv()

SECRET_AUTH_REQ = os.getenv('SECRET_AUTH_REQ')
SECRET_PASSWORD_REQ = os.getenv('SECRET_PASSWORD_REQ')


class BasicAuth(HttpBasicAuth):
    def authenticate(self, request, username, password):
        if username == SECRET_AUTH_REQ and password == SECRET_PASSWORD_REQ:
            return username


'''
Mesmo tirando o visto por último e online, e confirmação de leitura, se eu abrir uma foto de de visualização única, a outra pessoa vê que visualizei?

'''


def called_exception(e):
    if type(e) == Called.DoesNotExist:
        return 404, {"message": "Chamado não encontrado."}
    if type(e) == UserMobile.DoesNotExist:
        return 404, {"message": "Usuário não encontrado."}
    if type(e) == User.DoesNotExist:
        return 404, {"message": "Usuário não encontrado."}
    if type(e) == Problem.DoesNotExist:
        return 404, {"message": "Problema não encontrado."}
    if type(e) == City.DoesNotExist:
        return 404, {"message": "Município não encontrado."}
    if type(e) == ServiceOrder.DoesNotExist:
        return 404, {"message": "Ordem de serviço não encontrado."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=BasicAuth(), response={200: CalledOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Called"], )
def save_called(request, payload: CalledIn):
    try:
        problem = Problem.objects.get(id=payload.problem_id)

        toDict = payload.dict()
        images = payload.dict().pop("images")
        del toDict['images']
        called = Called.objects.create(**toDict)

        if payload.user_mobile_id:
            user = UserMobile.objects.get(id=payload.user_mobile_id)
            called.user_mobile = user
        if payload.user_id:
            user = User.objects.get(id=payload.user_id)
            called.user = user
        if payload.service_order_id != None:
            service_order = ServiceOrder.objects.get(
                id=payload.service_order_id)
            called.service_order = service_order

            if not service_order.calleds.filter(first_called=True).count() > 0:
                called.first_called = True

        called.problem = problem

        called.save()

        if payload.images:
            i = 0

            for image in images:
                i += 1
                image_converted = convert_image_base64_to_file(
                    image['file'], 'image_called' + str(called.id) + "_" + str(i))
                imageCalled = ImagesCalled()
                imageCalled.file = image_converted
                imageCalled.called = called
                imageCalled.save()

        called.images = called.image_called.all()

        return called
    except (Exception) as e:
        return called_exception(e)


@router.get("/", response=List[CalledOut], tags=["Called"], auth=BasicAuth())
@paginate(LimitOffsetPagination)
def search_called(request, city_id=0):
    '''
    Lista os chamados.
    '''
    try:
        calleds = Called.objects.filter(
            (Q(status="Aberto") | Q(status="Não atendido")))

        if city_id:
            calleds = calleds.filter(Q(city__id=city_id))

        for called in calleds:
            called.images = called.image_called.all()

        return calleds
    except (Exception) as e:
        print("aqui 2")
        print(e)
        return []


@router.get("/by-user/{user_id}/", response=List[CalledOut], tags=["Called"], auth=BasicAuth())
@paginate(LimitOffsetPagination)
def called_by_user(request, user_id: int):
    '''
    Lista os chamados por usuário.
    '''
    try:
        user = UserMobile.objects.get(id=user_id)
        calleds = Called.objects.filter(user__id=user.id)
        for called in calleds:
            called.images = called.image_called.all()

        return calleds
    except (Exception, UserMobile.DoesNotExist) as e:
        return []


@router.get("/by-service_order/{service_order_id}/", response=List[CalledOut], tags=["Called"], auth=BasicAuth())
@paginate(LimitOffsetPagination)
def called_by_service_order(request, service_order_id: int, search=""):
    '''
    Lista os chamados por ordem de serviço.
    '''
    try:
        service_order = ServiceOrder.objects.get(id=service_order_id)
        calleds = Called.objects.filter(service_order__id=service_order.id)
        if search:
            calleds = calleds.filter(Q(status__icontains=search) | Q(localization__icontains=search) | Q(
                city__name__icontains=search) | Q(problem__description__icontains=search))
        for called in calleds:
            called.images = called.image_called.all()

        return calleds
    except (Exception) as e:
        print(e)
        return []


@router.get("/{called_id}/", response={200: CalledOut, 404: MessageSchema, 500: MessageSchema}, tags=["Called"], auth=BasicAuth())
def detail_called(request, called_id: int):
    '''
    Recupera um chamado pelo ID.
    '''

    try:
        called = Called.objects.get(id=called_id)
        called.images = called.image_called.all()
        return called
    except (Exception, Called.DoesNotExist) as e:
        return called_exception(e)


@router.put("/{called_id}/", response={200: CalledOut, 404: MessageSchema, 500: MessageSchema}, tags=["Called"], auth=BasicAuth())
def update_called(request, payload: CalledUpdate, called_id: int, ):
    '''
    Atualiza um chamado pelo ID.
    '''

    try:
        called = Called.objects.get(id=called_id)

        if payload.problem_id:
            problem = Problem.objects.get(id=payload.problem_id)
            called.problem = problem
        '''
        if payload.user_id:
            user = UserMobile.objects.get(id=payload.user_id)
            called.user_mobile = user
        '''
        if payload.city_id:
            city = City.objects.get(id=payload.city_id)
            called.city = city
        if payload.status:
            called.status = payload.status
        if payload.lat:
            called.lat = payload.lat
        if payload.lng:
            called.lng = payload.lng
        if payload.localization:
            called.localization = payload.localization
        if payload.additional_information:
            called.additional_information = payload.additional_information

        called.save()
        called.images = called.image_called.all()
        return called
    except (Exception, Called.DoesNotExist, City.DoesNotExist, UserMobile.DoesNotExist, Problem.DoesNotExist) as e:
        return called_exception(e)


@router.delete("/{called_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Called"], auth=BasicAuth())
def delete_called(request, called_id: int, ):
    '''
    Deleta um chamado pelo ID.
    '''

    try:
        called = Called.objects.get(id=called_id)
        called.delete()
        return 200, {"message": "Chamado deletado com sucesso."}

    except (Exception, Called.DoesNotExist) as e:
        return called_exception(e)
