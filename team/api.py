from ninja import Router
from .models import Team
from town_hall.models import TownHall
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from manubrasil_backend.util.schemas import MessageSchema
from ninja_jwt.authentication import JWTAuth
from .schemas import TeamOut, TeamIn, TeamUpdate
from django.db.models import Q


router = Router()


def team_exception(e):
    if type(e) == Team.DoesNotExist:
        return 404, {"message": "Equipe não encontrado."}
    if type(e) == TownHall.DoesNotExist:
        return 404, {"message": "Prefeitura não encontrado."}
    return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/", auth=JWTAuth(), response={200: TeamOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Team"], )
def save_team(request, payload: TeamIn):
    try:
        town_hall = TownHall.objects.get(id=payload.town_hall_id)
        team = Team.objects.create(**payload.dict())
        team.town_hall = town_hall
        team.save()
        return team
    except (Exception, TownHall.DoesNotExist) as e:
        print(e)
        return team_exception(e)


@router.get("/", response=List[TeamOut], tags=["Team"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_team(request, name='', name_town_hall='', town_hall_id=0):
    '''
    Lista as equipes.
    '''

    teams = Team.objects.all()

    if town_hall_id:
        teams = teams.filter(town_hall__id=town_hall_id)
    if name or name_town_hall:
        teams = teams.filter(Q(name__icontains=name) | Q(
            town_hall__name__icontains=name_town_hall))
    return teams

@router.get("/by-town_hall/{town_hall_id}/", response=List[TeamOut], tags=["Team"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_team_by_town_hall(request, town_hall_id:int, name=''):
    '''
    Lista as equipes por prefeitura.
    '''
    try:
        town_hall = TownHall.objects.get(id=town_hall_id)
        teams = Team.objects.filter(town_hall_id=town_hall.id)
        if name:
            teams = teams.filter(name__icontains=name)

        return teams
    except:
        return []


@router.get("/{team_id}/", response={200: TeamOut, 404: MessageSchema, 500: MessageSchema}, tags=["Team"], auth=JWTAuth())
def detail_team(request, team_id: int):
    '''
    Recupera uma equipe pelo ID.
    '''

    try:
        team = Team.objects.get(id=team_id)
        return team
    except (Exception, Team.DoesNotExist) as e:
        return team_exception(e)


@router.put("/{team_id}/", response={200: TeamOut, 404: MessageSchema, 500: MessageSchema}, tags=["Team"], auth=JWTAuth())
def update_team(request, payload: TeamUpdate, team_id: int, ):
    '''
    Atualiza uma equipe pelo ID.
    '''

    try:
        team = Team.objects.get(id=team_id)

        if payload.name:
            team.name = payload.name
        if payload.town_hall_id:
            town_hall = TownHall.objects.get(id=payload.town_hall_id)
            team.town_hall = town_hall

        team.save()

        return team 
    except (Exception, Team.DoesNotExist, TownHall.DoesNotExist) as e:
        return team_exception(e)


@router.delete("/{team_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Team"], auth=JWTAuth())
def delete_team(request, team_id: int, ):
    '''
    Deleta uma equipe pelo ID.
    '''

    try:
        team = Team.objects.get(id=team_id)
        team.delete()
        return 200, {"message": "Equipe deletada com sucesso."}

    except (Exception, Team.DoesNotExist) as e:
        return team_exception(e)
