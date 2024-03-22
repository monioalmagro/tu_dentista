# Third-party Libraries
from django.core.mail import send_mail

# Own Libraries
from apps.psychology.models import ContactMe
from config.enviroment_vars import settings

SUBJECT_NEW_PROFESSIONAL = "Nuevo registro de un Profesional"
MESSAGE_NEW_PROFESSIONAL = "Nuevo registro de un Profesional"
RECIPIENT_LIST = [settings.DECIRES_EMAIL]
SUBJECT_CONTACT_ME = "Derivación"


async def prepare_data_contact_me(contact_me_instance: ContactMe):
    email_proff = contact_me_instance.user.email
    full_name = contact_me_instance.full_name
    email = contact_me_instance.email
    phone = contact_me_instance.phone
    user_message = contact_me_instance.message
    subject = SUBJECT_CONTACT_ME

    MESSAGE_CONTACT_ME = (
        f"El usuario {full_name}, solicitó una derivación con el "
        f"profesional {email_proff}, con el siguiente mensaje: "
        f"{user_message}. Datos del usuario: email: {email},  "
        f"telefono: {phone}"
    )

    recipient_list = RECIPIENT_LIST
    await prepare_and_send_email(
        subject, MESSAGE_CONTACT_ME, settings.DECIRES_EMAIL, recipient_list
    )
    await prepare_and_send_email(
        subject, MESSAGE_CONTACT_ME, settings.DECIRES_EMAIL, [str(email_proff)]
    )


async def prepare_and_send_email(
    subject: str, message: str, email_from: str, recipient_list: list
):
    send_mail(subject, message, email_from, recipient_list)


async def prepare_data_new_professional(new_professional):
    subject = SUBJECT_NEW_PROFESSIONAL
    message = MESSAGE_NEW_PROFESSIONAL
    email_from = settings.DECIRES_EMAIL
    recipient_list = RECIPIENT_LIST
    await prepare_and_send_email(subject, message, email_from, recipient_list)
