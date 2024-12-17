from ninja import Router
from .models import Problem
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from ninja_jwt.authentication import JWTAuth
from .schemas import ProblemIn, ProblemOut, ProblemUpdate
from django.db.models import Q


router = Router()


def problem_exception(e):
    if type(e) == Problem.DoesNotExist:
        return 404, {"message": "Problema não encontrado."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=JWTAuth(), response={200: ProblemOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Problem"], )
def save_problem(request, payload: ProblemIn):
    try:
        print(payload)
        problem = Problem.objects.create(**payload.dict())
        return problem
    except (Exception) as e:
        return problem_exception(e)


@router.get("/", response=List[ProblemOut], tags=["Problem"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_problem(request, search=''):
    '''
    Lista os problema.
    '''

    if search:
        problems = problems.filter(
            Q(description__icontains=search) | Q(type__icontains=search))

    else:
        problems = Problem.objects.all()

    return problems


@router.get("/{problem_id}/", response={200: ProblemOut, 404: MessageSchema, 500: MessageSchema}, tags=["Problem"], auth=JWTAuth())
def detail_problem(request, problem_id: int):
    '''
    Recupera um problema pelo ID.
    '''

    try:
        problem = Problem.objects.get(id=problem_id)
        return problem
    except (Exception, Problem.DoesNotExist) as e:
        return problem_exception(e)


@router.put("/{problem_id}/", response={200: ProblemOut, 404: MessageSchema, 500: MessageSchema}, tags=["Problem"], auth=JWTAuth())
def update_problem(request, payload: ProblemUpdate, problem_id: int, ):
    '''
    Atualiza um problema pelo ID.
    '''

    try:
        problem = Problem.objects.get(id=problem_id)

        if payload.description:
            problem.description = payload.description
        if payload.type:
            problem.type = payload.type

        problem.save()

        return problem
    except (Exception, Problem.DoesNotExist) as e:
        return problem_exception(e)


@router.delete("/{problem_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Problem"], auth=JWTAuth())
def delete_problem(request, problem_id: int, ):
    '''
    Deleta um problema pelo ID.
    '''

    try:
        problem = Problem.objects.get(id=problem_id)
        problem.delete()
        return 200, {"message": "Problema deletado com sucesso."}

    except (Exception, Problem.DoesNotExist) as e:
        return problem_exception(e)
