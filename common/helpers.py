from django.conf import settings
from django.core.mail import EmailMessage
from django.template import loader, Context
from django.utils import translation


def send_email(to_list, subject, message_template, message_context):
    translation.activate(settings.LANGUAGE_CODE)
    context = Context(message_context)
    message = loader.get_template(message_template).render(context)
    sender = settings.DEFAULT_FROM_EMAIL
    msg = EmailMessage(subject, message, sender, to_list)
    msg.content_subtype = "html"
    return msg.send(fail_silently=True)
