from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
import smtplib
from django.conf import settings
import os
from dotenv import load_dotenv
load_dotenv()

FRONT_BASE_URL = os.getenv('FRONT_BASE_URL')

#CONFIG
'''
EMAIL_REGISTER_ACCOUNT = "fdouglas7@gmail.com"
EMAIL_REGISTER_LOGIN = "fdouglas7@gmail.com"
EMAIL_REGISTER_PASSWORD = "yqgxdqokblqhhjik"
EMAIL_REGISTER_SMTP_PORT = "587"
EMAIL_REGISTER_SMTP_SERVER = "smtp.gmail.com"
'''

def send_email_recover_password_effective_opos(token, user):
    
    # create message object instance
    msg = MIMEMultipart()
    message = f"""
    <!DOCTYPE html>
    <html>
        <body>
        <p>
            Olá, tudo bem? <br>
            Recebos uma solicitação de recuperação de senha na plataforma ManuBrasil.
            Se não foi você, desconsidere este e-mail.
            <br>
            Este link é válido por 24h. Clique no link a seguir para continuar com a recuperação de senha:
            <h4>
                <a href="{FRONT_BASE_URL}recouver_password/receive-password-effective/{token}">Recuperar senha</a>
            </h4>
            <br>
            <hr>
            Muito obrigado.<br>
            <br>
            <b>Equipe ManuBrasil.<br>
        </p>
        </body>
    </html>
    """
    # setup the parameters of the message
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email
    msg['Subject'] = "[ManuBrasil] Recuperação de senha"
    # add in the message body
    msg.attach(MIMEText(message, 'html'))
    # create server
    server = smtplib.SMTP(
        f'{settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()


def send_email_recover_password_effective_manubrasil(code, user):
    
    msg = MIMEMultipart()
    message = f"""
    <!DOCTYPE html>
    <html>
        <body>
        <p>
            Olá, tudo bem? <br>
            Recebos uma solicitação de recuperação de senha na plataforma ManuBrasil.
            Se não foi você, desconsidere este e-mail.
            <br>
            Informe o código a seguir para ter acesso a sua conta. O código é válido por 24 horas.
            <h4>
                {code}
            </h4>
            <br>
            <hr>
            Muito obrigado.<br>
            <br>
            <b>Equipe ManuBrasil.<br>
        </p>
        </body>
    </html>
    """
    # setup the parameters of the message
    msg = MIMEMultipart()
    msg['From'] = settings.EMAIL_HOST_USER
    msg['To'] = user.email
    msg['Subject'] = "[MANUBRASIL] Recuperação de senha"
    # add in the message body
    msg.attach(MIMEText(message, 'html'))
    # create server
    server = smtplib.SMTP(
        f'{settings.EMAIL_HOST}:{settings.EMAIL_PORT}')
    server.starttls()
    # Login Credentials for sending the mail
    server.login(settings.EMAIL_HOST_USER, settings.EMAIL_HOST_PASSWORD)
    # send the message via the server.
    server.sendmail(msg['From'], msg['To'], msg.as_string())
    server.quit()