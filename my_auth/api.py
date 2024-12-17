from ninja import Router
from .models import *
from ninja.pagination import paginate, LimitOffsetPagination
from typing import List
from django.contrib.auth import login
from django.utils import timezone
from django.db.models import Q
from django.db.utils import IntegrityError
from manubrasil_backend.util.schemas import MessageSchema
from manubrasil_backend.util.util_functions import convert_image_base64_to_file
from ninja_jwt.authentication import JWTAuth
from .schemas import *
from .email_manager import send_email_recover_password_effective_opos, send_email_recover_password_effective_manubrasil
import bcrypt
from dotenv import load_dotenv


router = Router()


def user_exception(e):
    if type(e) == User.DoesNotExist:
        return 404, {"message": "Usuário não encontrado."}
    elif type(e) == Team.DoesNotExist:
        return 404, {'message': 'Equipe não encontrada.'}
    elif type(e) == City.DoesNotExist:
        return 404, {'message': 'Município não encontrado.'}
    elif type(e) == TownHall.DoesNotExist:
        return 404, {'message': 'Prefeitura não encontrada.'}
    if type(e) == TokenRecoverPassword.DoesNotExist:
        return 404, {"message": "Token inválido."}
    else:
        return 500, {"message": "Erro inesperado: {}.".format(str(e))}


load_dotenv()

SECRET_AUTH_REQ = os.getenv('SECRET_AUTH_REQ')
SECRET_PASSWORD_REQ = os.getenv('SECRET_PASSWORD_REQ')



@router.get("/users/", response=List[UserOutSchema], tags=["Auth"], auth=JWTAuth())
@paginate(LimitOffsetPagination)
def search_user(request, name='', city='', name_team="", name_city="", name_town_hall="",  email=""):
    '''
    Lista os usuários por meio de filtro de nome e cidade, não havendo é retornado todos os usuários.
    '''

    users = User.objects.all()

    if city:
        users = users.filter(city__nome__icontains=city)

    if name_team or name_city or name_town_hall or email or name:
        users = users.filter(Q(name__icontains=name) | Q(city__name__icontains=name_city) | Q(town_hall__name__icontains=name_town_hall) |
                             Q(team__name__icontains=name_team) | Q(email__icontains=email))
    return users


@router.get("/users/{int:user_id}/", response={200: UserOutSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Auth"], auth=JWTAuth())
def get_user(request, user_id: int):
    '''
    Retorna um usuário específico do sistema a partir do ID do mesmo.
    '''
    try:
        user = User.objects.get(id=user_id)
        return user
    except (Exception, User.DoesNotExist) as e:
        return user_exception(e)


@router.get("/username/{str:username}/", response={200: UserOutSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Auth"], auth=JWTAuth())
def user_by_username(request, username: str):
    '''
    Retorna um usuário específico do sistema a partir do username do mesmo.
    '''
    try:
        user = User.objects.get(username=username)
        return user
    except (Exception, User.DoesNotExist) as e:
        return user_exception(e)


@router.post("/users/mobile/verify-code/", auth=None, response={200: UserMobileOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Mobile"])
def verify_code_mobile(request, payload: UserMobileRecoverPassword):
    '''
    Verifica um código enviado por e-mail para recuperação de senha.
    '''
    try:
        if not payload.code:
            return 400, {"message": "Certifique-se de informar a nova senha (password)."}

        if not payload.email:
            return 400, {"message": "Certifique-se de informar o e-mail)."}

        code_recover = CodeRecoverPassword.objects.get(
            Q(code=payload.code) & Q(user__email=payload.email))
        if (timezone.now() - code_recover.create_at).days > 1:
            code_recover.delete()
            return 401, {"message": "Código expirado. Por favor, tente gerar um novo código."}
        user = code_recover.user
        code_recover.delete()

        return user

    except (Exception, CodeRecoverPassword.DoesNotExist) as e:
        if type(e) == CodeRecoverPassword.DoesNotExist:
            return 404, {"message": "Código utilizado ou inexistente, por favor, gerar um novo código."}
        return 500, {"message": "Erro inesperado {}".format(str(e))}


@router.post("/users/recover-password/effective/", auth=None, response={200: MessageSchema, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Auth"])
def recover_password(request, payload: UserRecoverPassword):
    '''
    Altera a senha de um determinado usuário por meio de um token enviado por e-mail.
    '''
    try:
        if not payload.token:
            return 400, {"message": "Token não informado."}
        if not payload.password:
            return 400, {"message": "Certifique-se de informar a nova senha (password)."}
        if not payload.confirm_password:
            return 400, {"message": "Certifique-se de informar a confirmação da nova senha (confirm_password)."}

        if payload.password != payload.confirm_password:
            return 400, {"message": "As senhas não conferem. Por favor, verifique se a senhas são iguais."}

        token_recover = TokenRecoverPassword.objects.get(token=payload.token)

        if ((timezone.localtime(timezone.now())) - token_recover.create_at).days > 1:
            token_recover.delete()
            return 401, {"message": "Token expirado. Por favor, tente gerar um novo token."}

        user = token_recover.user

        user.set_password(payload.password)

        token_recover.delete()

        return 200, {"message": "Senha alterada com sucesso."}

    except (Exception, TokenRecoverPassword.DoesNotExist) as e:
        print(e)
        return user_exception(e)


@router.post("/users/mobile/send-email-recover-password/", auth=None, response={200: MessageSchema, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Mobile"])
def send_email_recover_password_mobile(request, payload: UserSendEmailRecoverPasswordMobile):
    '''
    Envia um e-mail com um código para o endereço de e-mail informado.
    '''
    try:
        if not payload.email:
            return 400, {"message": "Certifique-se de informar o e-mail."}

        user = UserMobile.objects.get(email=payload.email)

        code = generate_code_recover_password_mobile(user)

        send_email_recover_password_effective_manubrasil(code, user)

        return 200, {"message": "E-mail enviado com sucesso para {}".format(payload.email)}
    except (Exception, UserMobile.DoesNotExist) as e:
        if type(e) == UserMobile.DoesNotExist:
            return 404, {"message": "Nenhum usuário para este e-mail."}

        return 500, {"message": "Erro inesperado {}".format(e)}


@router.post("/users/recover-password/", auth=None, response={200: MessageSchema, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Auth"])
def send_email_recover_password(request, payload: UserSendEmailRecoverPassword):
    '''
    Envia um e-mail com um token para o endereço de e-mail informado.
    '''
    try:
        if not payload.email:
            return 400, {"message": "Certifique-se de informar o e-mail."}

        user = User.objects.get(email=payload.email)

        token = generate_token_recover_password(user)

        send_email_recover_password_effective_opos(token, user)

        return 200, {"message": "E-mail enviado com sucesso para {}".format(payload.email)}
    except (Exception, User.DoesNotExist) as e:
        print(e)
        return user_exception(e)


@router.post("/users/authenticate/", auth=None, response={200: UserOutSchema, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Auth"])
def authenticate_user(request, payload: UserAuthenticate):
    '''
    Autentica um usuário por meio de username e password.
    '''
    try:
        if not payload.username:
            return 400, {"message": "Certifique-se de informar o nome de usuário (username)."}
        if not payload.password:
            return 400, {"message": "Certifique-se de informar a senha (password)."}

        user = User.objects.get(username=payload.username)
        if user.check_password(payload.password):
            login(request, user)
            return user
        else:
            return 401, {"message": "Senha incorreta. Por favor, verifique sua senha."}

    except (Exception, User.DoesNotExist) as e:
        return user_exception(e)


@router.post("/users/mobile/authenticate/", auth=None, response={200: UserMobileOut, 500: MessageSchema, 400: MessageSchema, 404: MessageSchema, 401: MessageSchema}, tags=["Mobile"])
def authenticate_user_mobile(request, payload: UserMobileAuthenticate):
    '''
    Autentica um usuário mobile por meio de e-mail e senha.
    '''
    try:
        if not payload.email:
            return 400, {"message": "Certifique-se de informar o e-mail de usuário (email)."}
        if not payload.password:
            return 400, {"message": "Certifique-se de informar a senha (password)."}

        user = UserMobile.objects.get(email=payload.email)
        passwordBytes = bytes(payload.password, "utf-8")
        check = bcrypt.checkpw(passwordBytes, user.password.encode("utf-8"))

        if check:
            return user
        else:
            return 401, {"message": "E-mail ou senha incorretos."}

    except (Exception, UserMobile.DoesNotExist) as e:
        if type(e) == UserMobile.DoesNotExist:
            return 404, {"message": "E-mail ou senha incorretos."}
        else:
            return 500, {"message": "Erro inesperado: {}.".format(str(e))}


@router.post("/users/",  response={200: UserOutSchema, 500: MessageSchema, 406: MessageSchema, 404: MessageSchema, 400: MessageSchema}, tags=["Auth"], auth=JWTAuth())
def post_user(request, payload: UserIn):
    '''
    Adiciona um novo usuário ao sistema.
    '''
    try:
        if not payload.team:
            return 400, {"message": "Certifique-se de informar a equipe."}
        if not payload.city:
            400, {"message": "Certifique-se de informar a cidade."}
        if not payload.town_hall:
            return 400, {"message": "Certifique-se de informar a prefeitura."}
        if not payload.name:
            return 400, {"message": "Certifique-se de informar o nome (name)."}
        if not payload.email:
            400, {"message": "Certifique-se de informar o e-mail (email)."}
        if not payload.type:
            return 400, {"message": "Certifique-se de informar o tipo."}

        if payload.password and payload.confirm_password and payload.password != "" and payload.confirm_password:
            if payload.password != payload.confirm_password:
                return 400, {"message": "As senhas não conferem. Por favor, verifique as senhas."}

        team = Team.objects.get(id=payload.team)
        city = City.objects.get(id=payload.city)
        town_hall = TownHall.objects.get(id=payload.town_hall)

        if verify_email(payload.email, None):

            user = User.objects.create_user(
                username=payload.email,
                email=payload.email,
                type=payload.type,
                name=payload.name,
                password=payload.password,
                team=team,
                city=city,
                town_hall=town_hall,
            )
            if payload.photo and payload.photo != "":
                photo = convert_image_base64_to_file(
                    payload.photo, "user_" + str(user.id))

            if payload.photo:
                user.photo = photo
            user.save()
        else:
            return 406, {'message': 'E-mail já presente no sistema.'}

        return user
    except (Exception, Team.DoesNotExist, City.DoesNotExist, TownHall.DoesNotExist, IntegrityError) as e:
        return user_exception(e)


@router.post("/users/mobile/",  response={200: UserMobileOut, 500: MessageSchema, 406: MessageSchema, 404: MessageSchema, 400: MessageSchema}, tags=["Mobile"])
def post_user_mobile(request, payload: UserMobileIn):
    '''
    Adiciona um novo usuário mobile ao sistema.
    '''
    try:
        if not payload.email:
            return 400, {"message": "Certifique-se de informar o e-mail (email)."}
        if not payload.full_name:
            return 400, {"message": "Certifique-se de informar o nome completo (full_name)."}
        if not payload.password:
            return 400, {"message": "Certifique-se de informar a senha (password)."}
        if not payload.type:
            return 400, {"message": "Certifique-se de informar o tipo (type)."}
        if not payload.cpf:
            return 400, {"message": "Certifique-se de informar o CPF (cpf)."}
        if not payload.number_phone:
            return 400, {"message": "Certifique-se de informar o número de telefone (number_phone)."}

        if verify_email_mobile(payload.email, None):
            password = payload.password
            bytes = password.encode('utf-8')
            salt = bcrypt.gensalt()
            hash = bcrypt.hashpw(bytes, salt)
            passwodTest = hash.decode('utf-8')

            user = UserMobile.objects.create(
                email=payload.email,
                type=payload.type,
                full_name=payload.full_name,
                password=passwodTest,
                cpf=payload.cpf,
                number_phone=payload.number_phone
            )
            return user

        else:
            return 406, {'message': 'E-mail já presente no sistema.'}

    except (Exception) as e:
        return 500, {"message": "Erro inesperado: " + str(e) + "."}


@router.put("/users/mobile/update-password",  response={200: UserMobileOut, 500: MessageSchema, 406: MessageSchema, 404: MessageSchema, 400: MessageSchema}, tags=["Mobile"])
def update_password_user_mobile(request, payload: UserMobileUpdatePassword):
    '''
    Altera a senha de um usuário mobile do sistema.
    '''
    try:

        user = UserMobile.objects.get(id=payload.user_id)

        if payload.new_password != payload.confirm_new_password:
            return 400, {"message": "As senhas não são iguais."}

        new_password = payload.new_password
        bytes = new_password.encode('utf-8')
        salt = bcrypt.gensalt()
        hash = bcrypt.hashpw(bytes, salt)
        new_password_hash = hash.decode('utf-8')
        user.password = new_password_hash
        user.save()
        return user
    except (Exception, UserMobile.DoesNotExist) as e:
        if type(e) == UserMobile.DoesNotExist:
            return 404, {"message": "Usuário não encontrado."}
        return 500, {"message": "Erro inesperado: " + str(e) + "."}


@router.put("/mobile/users/{int:user_id}/",  response={200: UserMobileOut, 500: MessageSchema, 406: MessageSchema, 404: MessageSchema, 400: MessageSchema}, tags=["Mobile"])
def put_user_mobile(request, payload: UserMobileUpdateSchema, user_id: int):
    '''
    Atualiza um novo usuário mobile ao sistema.
    '''
    try:

        user = UserMobile.objects.get(id=user_id)
        if payload.cpf:
            user.cpf = payload.cpf
        if payload.number_phone:
            user.number_phone = payload.number_phone
        if payload.full_name:
            user.full_name = payload.full_name
        if payload.type:
            user.type = payload.type

        user.save()

        if payload.email:
            if verify_email_mobile(payload.email, user=user):
                user.email = payload.email
                user.save
            else:
                return 406, {'message': 'E-mail já presente no sistema.'}
        return user
    except (Exception, UserMobile.DoesNotExist) as e:
        if type(e) == UserMobile.DoesNotExist:
            return 404, {"message": "Usuário não encontrado."}
        return 500, {"message": "Erro inesperado: " + str(e) + "."}


@router.put("/users/{int:user_id}/", response={200: UserOutSchema, 404: MessageSchema, 500: MessageSchema, 406: MessageSchema, 400: MessageSchema}, tags=["Auth"], auth=JWTAuth())
def put_user(request, user_id: int, payload: UserUpdateSchema):
    '''
    Atualiza um usuário específico do sistema a partir do ID do mesmo.
    '''
    try:
        user = User.objects.get(id=user_id)
        print("payload")
        print(payload)

        if payload.team != None:
            team = Team.objects.get(id=payload.team)
            user.team = team
        if payload.city != None:
            city = City.objects.get(id=payload.city)
            user.city = city
        if payload.city != None:
            town_hall = TownHall.objects.get(id=payload.town_hall)
            user.town_hall = town_hall
        if payload.photo != None and payload.photo != '':
            image = convert_image_base64_to_file(
                payload.photo, "user_" + str(user.id))
            user.photo = image
        if payload.name != None:
            user.name = payload.name
        if payload.email != None:
            if verify_email(payload.email, user):
                user.email = payload.email
                user.username = payload.email
            else:
                return 406, {'message': 'E-mail já presente no sistema.'}
        if payload.type != None:
            user.type = payload.type

        user.save()
        return user
    except (Exception) as e:
        print(e)
        return user_exception(e)


@router.put("/users/change-password/{int:user_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema, 400: MessageSchema}, tags=["Auth"], auth=JWTAuth())
def update_password(request, user_id: int, payload: UserUpdatePassword):
    try:
        if not payload.password:
            return 400, {"message", "Certifique-se de informar a senha (password)."}
        if not payload.confirm_password:
            return 400, {"message": "Certifique-se de informar a carfirmação de senha (confirm_password)"}
        if payload.password != payload.confirm_password:
            return 400, {"message": "As senhas não correspondem. Por favor, verifique a senha e a confirmação."}
        user = User.objects.get(id=user_id)

        user.set_password(payload.password)
        user.save()
        return 200, {"message": "Senha alterada com sucesso."}
    except (Exception, User.DoesNotExist) as e:
        return user_exception(e)


@router.delete("/users/{int:user_id}/", response={200: MessageSchema, 404: MessageSchema, 500: MessageSchema}, tags=["Auth"], auth=JWTAuth())
def delete_user(request, user_id: int):
    '''
    Deleta um usuário específico do sistema a partir do ID do mesmo.
    '''
    try:
        user = User.objects.get(id=user_id)
        user.delete()
        return 200, {"message": "Usuário deletado com sucesso."}
    except (Exception, User.DoesNotExist) as e:
        return user_exception(e)
