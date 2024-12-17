from ninja import Router
from .models import State
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from ninja_jwt.authentication import JWTAuth
from .schemas import StateIn, StateOut, StateUpdate


router = Router()


def state_exception(e):
    if type(e) == State.DoesNotExist:
        return 404, {"message": "Estado não encontrado."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=JWTAuth(), response={200: StateOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["State"], )
def save_state(request, payload: StateIn):
    try:
        state = State.objects.create(**payload.dict())
        return state
    except (Exception) as e:
        return state_exception(e)


@router.get("/", response=List[StateOut], tags=["State"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_state(request, name=''):
    '''
    Lista os estados.
    '''

    if name:
        states = State.objects.filter(name__icontains=name)
    else:
        states = State.objects.all()

    return states


@router.get("/{state_id}/", response={200: StateOut, 404: MessageSchema, 500: MessageSchema}, tags=["State"], auth=JWTAuth())
def detail_state(request, state_id: int):
    '''
    Recupera um estado pelo ID.
    '''

    try:
        state = State.objects.get(id=state_id)
        return state
    except (Exception, State.DoesNotExist) as e:
        return state_exception(e)


@router.put("/{state_id}/", response={200: StateOut, 404: MessageSchema, 500: MessageSchema}, tags=["State"], auth=JWTAuth())
def update_state(request, payload: StateUpdate, state_id: int, ):
    '''
    Atualiza um estado pelo ID.
    '''

    try:
        state = State.objects.get(id=state_id)

        if payload.name:
            state.name = payload.name

        state.save()

        return state
    except (Exception, State.DoesNotExist) as e:
        return state_exception(e)


@router.delete("/{state_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["State"], auth=JWTAuth())
def delete_state(request, state_id: int, ):
    '''
    Deleta um estado pelo ID.
    '''

    try:
        state = State.objects.get(id=state_id)
        state.delete()
        return 200, {"message": "Estado deletado com sucesso."}

    except (Exception, State.DoesNotExist) as e:
        return state_exception(e)
