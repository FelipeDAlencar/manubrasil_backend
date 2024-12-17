from ninja import Router
from .models import ServiceOrder
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from ninja_jwt.authentication import JWTAuth
from .schemas import ServiceOrderIn, ServiceOrderOut, ServiceOrderUpdate
from called.models import Called
from datetime import datetime, timedelta
from django.db.models import Q
from my_auth.models import User
from problem.models import Problem
from city.models import City
from django.db import transaction
from django.utils.timezone import make_aware


router = Router()


def so_exception(e):
    if type(e) == ServiceOrder.DoesNotExist:
        return 404, {"message": "Ordem de serviço não encontrada."}
    if type(e) == Problem.DoesNotExist:
        return 404, {"message": "Problema não encontrado."}
    if type(e) == City.DoesNotExist:
        return 404, {"message": "Município não encontrada."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=JWTAuth(), response={200: ServiceOrderOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["ServiceOrder"], )
def save_service_order(request, payload: ServiceOrderIn):
    try:
        with transaction.atomic():
            toDict = payload.dict()
            model_data = {key: value for key,
                          value in toDict.items() if hasattr(ServiceOrder, key)}

            service_order = ServiceOrder.objects.create(**model_data)

            user = User.objects.get(id=request.user.id)
            city = City.objects.get(id=payload.city_id)
            problem = Problem.objects.get(id=payload.problem_id)
            service_order.save()
            i = 1

            if payload.calleds_ids != None and len(payload.calleds_ids) > 0:
                for id in payload.calleds_ids:

                    called = Called.objects.get(id=id)
                    called.service_order = service_order
                    if i == 1:

                        i += 1
                        called.first_called = True
                    called.save()
            else:
                called = Called()
                called.localization = payload.localization
                called.lat = payload.lat
                called.lng = payload.lng
                called.additional_information = service_order.description
                called.user = user
                called.problem = problem
                called.city = city
                called.service_order = service_order
                called.first_called = True
                called.save()

            return service_order
    except (Exception) as e:
        print(e)
        return so_exception(e)


@router.get("/", response=List[ServiceOrderOut], tags=["ServiceOrder"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_service_order(request, status="", start_date="", end_date="", city_id=0, neighborhood_id=0, type="",):
    '''
    Lista as ordens de serviço.
    '''
    try:
        sos = ServiceOrder.objects.all()

        if status:
            print("aqui 1")
            print(status)
            sos = sos.filter(status=status)

        if start_date and end_date:
            start_date_converted = datetime.strptime(
                start_date, "%d/%m/%Y").date()
            end_date_converted = datetime.strptime(
                end_date, "%d/%m/%Y").date() + timedelta(days=1)
            sos = sos.filter(Q(create_at__gte=start_date_converted) & Q(
                create_at__lte=end_date_converted))
        if city_id:
            sos = sos.filter(calleds__city__id=city_id).distinct()

        if neighborhood_id:
            print("aqui 2")
            sos = sos.filter(calleds__city__neighborhood__id=neighborhood_id).distinct()

        if type:
            print("aqui 3")
            sos = sos.filter(calleds__problem__type=type)
        
        for so in sos:
            first_called = (so.calleds.filter(first_called=True))
            if first_called:
                so.first_called = first_called[0]
        #/api/service-order/?city_id=2&neighborhood_id=1&status=&type=
        #/api/service-order/?city_id=0&neighborhood_id=1
        return sos
    except (Exception) as e:
        print(e)
        return []


'''
@router.get("/ordens/por-bairro/", response=List[ServiceOrderOut], tags=["ServiceOrder"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def list_os_by_neighborhood(request, data_inicial="", data_final="", bairro=0, cidade=0):

    Lista as ordens por bairro em um determinado período.


    sos = ServiceOrder.objects.all()
    if bairro:
        sos = sos.filter(poste__bairro__id=bairro)

    if data_inicial and data_final:
        date_initial_converted = datetime.strptime(
            data_inicial, "%d/%m/%Y").date()
        date_final_converted = datetime.strptime(
            data_final, "%d/%m/%Y").date() + timedelta(days=1)
        sos = sos.filter(Q(criada_em__gte=date_initial_converted) & Q(
            criada_em__lte=date_final_converted))

    return sos
'''


@router.get("/by-problem/{problem_id}/", response=List[ServiceOrderOut], tags=["ServiceOrder"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def so_by_problem(request, problem_id: int, start_date="", end_date="", ):
    '''
    Lista as ordens por problema em um determinado período.
    '''
    # calleds__first_called__problem__id=problem_id
    sos = ServiceOrder.objects.filter(
        Q(calleds__first_called=True) & Q(calleds__problem__id=problem_id))

    if start_date and end_date:
        user = User.objects.get(id=request.user.id)
        start_date_converted = datetime.strptime(
            start_date, "%d/%m/%Y").date()
        end_date_converted = datetime.strptime(
            end_date, "%d/%m/%Y").date() + timedelta(days=1)
        sos = sos.filter(Q(create_at__gte=start_date_converted) & Q(
            create_at__lte=end_date_converted) & Q(calleds__city__id=user.city.id))
    for so in sos:
        so.first_called = so.calleds.get(first_called=True)

    sos = sos.filter().distinct()
    return sos


@router.get("/closing-of-the-month/", response=List[ServiceOrderOut], tags=["ServiceOrder"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def so_by_closing_of_the_month(request, year=0, month=0):
    try:
        '''
        Lista as ordens por atendidas por um determinado período.

        '''
        sos = []
        if year != 0 and month != 0:
            user = User.objects.get(id=request.user.id)
            sos = ServiceOrder.objects.filter(Q(create_at__year=year) & Q(
                create_at__month=month) & Q(status="Concluída") & Q(calleds__city__id=user.city.id))

        for so in sos:
            so.first_called = so.calleds.get(first_called=True)
        return sos
    except (Exception) as e:
        print(e)


@router.get("/orders-service-time/", response=List[ServiceOrderOut], tags=["ServiceOrder"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def so_orders_service_time(request, service_time=0):
    '''
    Lista as ordens atendidas por um determinado período.
    '''
    user = User.objects.get(id=request.user.id)

    sos = []
    if service_time == 24:
        in_24h = datetime.now() - timedelta(days=1)
        sos = ServiceOrder.objects.filter(Q(open_date__gte=in_24h) & Q(
            status="Aberta") & Q(first_called__city__id=user.city.id))
    elif service_time == 72:
        in_72h = datetime.now() - timedelta(days=3)
        sos = ServiceOrder.objects.filter(Q(open_date__gte=in_72h) & Q(
            status="Aberta") & Q(first_called__city__id=user.city.id))
    else:
        in_more_72h = datetime.now() - timedelta(days=3)
        sos = ServiceOrder.objects.filter(Q(open_date__lt=in_more_72h) & Q(
            status="Aberta") & Q(first_called__city__id=user.city.id))
    for so in sos:
        so.first_called = so.calleds.get(first_called=True)
    return sos


@router.get("/{service_order_id}/", response={200: ServiceOrderOut, 404: MessageSchema, 500: MessageSchema}, tags=["ServiceOrder"], auth=JWTAuth())
def detail_service_order(request, service_order_id: int):
    '''
    Recupera um ordem de serviço pelo ID.
    '''

    try:
        service_order = ServiceOrder.objects.get(id=service_order_id)

        service_order.first_called = service_order.calleds.get(
            first_called=True)
        return service_order
    except (Exception, ServiceOrder.DoesNotExist) as e:
        print(e)
        return so_exception(e)


@router.put("/{service_order_id}/", response={200: ServiceOrderOut, 404: MessageSchema, 400: MessageSchema, 500: MessageSchema}, tags=["ServiceOrder"], auth=JWTAuth())
def update_service_order(request, payload: ServiceOrderUpdate, service_order_id: int, ):
    '''
    Altera uma Ordem de Serviço no Sistema.
    '''
    try:

        user = User.objects.get(id=request.user.id)
        service_order = ServiceOrder.objects.get(id=service_order_id)

        if payload.status:
            if user.type != "Administrador":
                return 400, {"message": "Você não tem permissão para alterar o status da ordem de serviço."}
            service_order.status = payload.status
            if payload.status == "Aberta":
                service_order.open_date = datetime.now()
        if payload.description:
            service_order.description = payload.description

        if payload.problem_id:
            problem = Problem.objects.get(id=payload.problem_id)
            service_order.problem = problem

        if payload.city_id:
            city = City.objects.get(id=payload.city_id)
            service_order.city = city

        i = 1
        if payload.calleds_ids != None and len(payload.calleds_ids) > 0:
            Called.objects.filter(service_order__id=service_order.id).update(
                service_order=None)
            for id in payload.calleds_ids:
                called = Called.objects.get(id=id)
                called.service_order = service_order
                if i == 1:
                    i += 1
                    called.first_called = True
                called.save()
        else:
            Called.objects.filter(service_order__id=service_order.id).update(
                service_order=None)
            called = Called()
            called.localization = payload.localization
            called.lat = payload.latitude
            called.lng = payload.longitude
            called.additional_information = service_order.description
            called.user = user
            called.problem = problem
            called.city = city
            called.service_order = service_order
            called.first_called = True
            called.save()

        called = service_order.calleds.get(first_called=True)
        if payload.latitude:
            called.lat = payload.latitude

        if payload.longitude:
            called.lng = payload.longitude

        if payload.localization:
            called.localization = payload.localization

        called.save()
        service_order.save()
        return service_order
    except (Exception) as e:
        print(e)
        return so_exception(e)


'''
@router.delete("/{service_order_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["ServiceOrder"], auth=JWTAuth())
def delete_service_order(request, service_order_id: int, ):
    
    Deleta um ordem de serviço pelo ID.
    

    try:
        so = ServiceOrder.objects.get(id=service_order_id)
        so.delete()
        return 200, {"message": "Ordem de serviço deletada com sucesso."}

    except (Exception, ServiceOrder.DoesNotExist) as e:
        return so_exception(e)
'''
