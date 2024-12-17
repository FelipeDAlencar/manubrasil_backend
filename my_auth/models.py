from django.db import models
from django.contrib.auth.models import User as DjangoUser
import os
from django.conf import settings
import secrets
import random
from city.models import City
from town_hall.models import TownHall
from team.models import Team


class User(DjangoUser):
    name = models.CharField(max_length=250, blank=False, null=False)
    team = models.ForeignKey(Team, on_delete=models.SET_NULL, null=True, blank=False, related_name="team_user", verbose_name="Equipe")
    city = models.ForeignKey(City, on_delete=models.SET_NULL, null=True, blank=False, related_name="city_user", verbose_name="Cidade")
    town_hall = models.ForeignKey(TownHall, on_delete=models.SET_NULL, null=True, blank=False, related_name="town_hall_user", verbose_name="Prefeitura")


    photo = models.ImageField(upload_to="photos/", null=True, blank=True)
    type_choices =  (
        ("Usuário", 'Usuário'),
        ("Colaborador", 'Colaborador'),
        ("Coordenador de Equipe", 'Coordenador de Equipe'),
        ("Administrador", 'Administrador'),
    )
    type = models.CharField(
        max_length=50, choices=type_choices, default="Usuário")
    
    def save(self, *args, **kwargs):
        if self.photo:
            if not os.path.exists(os.path.join(settings.MEDIA_ROOT, 'photos/')):
                os.makedirs(os.path.join(settings.MEDIA_ROOT,'photos/')) 
        super(User, self).save(*args, **kwargs)
        
    def __str__(self) -> str:
        return self.username + " - " + str(self.id)

class TokenRecoverPassword(models.Model):
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, blank=False, null=False)
    token = models.CharField(max_length=200, blank=False, null=False)
    create_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.user.username + " - " + str(self.create_at)

def generate_token() -> str:
    """
        Gera um token único.
    """
    while True:
        token = secrets.token_urlsafe(70)
        # verifica se o token ja existe nos usuarios
        if not TokenRecoverPassword.objects.filter(token=token).exists():
            return token

def generate_token_recover_password(user):
    try:
        tokens = TokenRecoverPassword.objects.filter(user__id=user.id)
        tokens.delete()

        token = generate_token()

        user_token = User.objects.get(id=user.id)

        TokenRecoverPassword.objects.create(
            user=user_token, token=token)
        return token
    except (Exception, User.DoesNotExist) as e:
        if type(e) == User.DoesNotExist:
            return "Usuário não encontrado para criação do token."
        else:
            return "Erro inesperado: " + str(e)

def verify_email(email, user : None)-> bool:
    if user:
        if User.objects.filter(email=email).exclude(id=user.id).count() > 0:
            return False
        return True
    else:
        if User.objects.filter(email=email).count() > 0:
            return False
        return True



class UserMobile(models.Model):
    email = models.EmailField(blank=False, null=False, max_length=200)
    full_name = models.CharField(max_length=250, blank=False, null=False)
    cpf = models.CharField(blank=False, null=False, max_length=14)
    number_phone = models.CharField(blank=False, null=False, max_length=14)
    password = models.CharField(blank=False, null=False, max_length=250)
    active = models.BooleanField(default=True)
    type_choices = (
        ("Usuário", 'Usuário'),
        ("Colaborador", 'Colaborador'),
        ("Coordenador de Equipe", 'Coordenador de Equipe'),
        ("Administrador", 'Administrador'),
    )
    type = models.CharField(
        max_length=50, choices=type_choices, default="Usuário")

class CodeRecoverPassword(models.Model):
    code = models.IntegerField()
    create_at = models.DateTimeField(auto_now_add=True)
    user  = models.ForeignKey(
        UserMobile, on_delete=models.CASCADE, null=True, related_name='code_recover_user')


def verify_email_mobile(email, user: None) -> bool:
    if user:
        if UserMobile.objects.filter(email=email).exclude(id=user.id).count() > 0:
            return False
        return True
    else:
        if UserMobile.objects.filter(email=email).count() > 0:
            return False
        return True

def generate_code() -> str:
   
    while True:
        code = random.randrange(1000, 9000, 3)
        if not CodeRecoverPassword.objects.filter(code=code).exists():
            return code
        
def generate_code_recover_password_mobile(user):
    try:
        codes = CodeRecoverPassword.objects.filter(user__id=user.id)
        codes.delete()

        code = generate_code()

        user_code = UserMobile.objects.get(id=user.id)

        CodeRecoverPassword.objects.create(
            user=user_code, code=code)
        return code
    
    except (Exception, UserMobile.DoesNotExist) as e:
        if type(e) == UserMobile.DoesNotExist:
            return "Usuário não encontrado para criação do código."
        else:
            return "Erro inesperado: " + str(e)
        



