from fastapi_mail import FastMail, MessageSchema, ConnectionConfig
from app.config.settings import settings 

'''conf = ConnectionConfig(
    MAIL_USERNAME = settings.MAIL_USERNAME,
    MAIL_PASSWORD = settings.MAIL_PASSWORD,
    MAIL_FROM = settings.MAIL_FROM,
    MAIL_PORT = settings.MAIL_PORT,
    MAIL_SERVER = settings.MAIL_SERVER,
    MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
    MAIL_STARTTLS = True,
    MAIL_SSL_TLS = False,
    USE_CREDENTIALS = True
)'''





try:
    conf = ConnectionConfig(
        MAIL_USERNAME = settings.MAIL_USERNAME,
        MAIL_PASSWORD = settings.MAIL_PASSWORD,
        MAIL_FROM = settings.MAIL_FROM,
        MAIL_PORT = settings.MAIL_PORT,
        MAIL_SERVER = settings.MAIL_SERVER,
        MAIL_FROM_NAME = settings.MAIL_FROM_NAME,
        MAIL_STARTTLS = True,   
        MAIL_SSL_TLS = False,   
        USE_CREDENTIALS = True,
        VALIDATE_CERTS = True
    )
except Exception as e:
    conf = None

async def send_return_confirmation_email(email_to: str, user_name: str, book_title: str):
    if not conf:
        print("Email configuration is invalid. Skipping email send.")
        return
        
    try:
        message = MessageSchema(
            subject="Book Returned Successfully!",
            recipients=[email_to],
            body=f"Hi {user_name}, aapne '{book_title}' book successfully return kar di hai. Thank you!",
            subtype="html"
        )
        fm = FastMail(conf)
        await fm.send_message(message)
    except Exception as e:
        print(f"Error sending email to {email_to}: {e}")