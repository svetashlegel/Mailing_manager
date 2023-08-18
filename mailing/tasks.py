from django.conf import settings
from django.core.mail import send_mail
from background_task import background

from mailing.models import Mail


@background
def send_newsletter(mail_id):
    clients_list = []
    mail_item = Mail.objects.get(pk=mail_id)
    for client in mail_item.clients.all():
        clients_list.append(client.email)
    print(clients_list)
    send_mail(
        mail_item.title,
        mail_item.content,
        settings.EMAIL_HOST_USER,
        clients_list
    )


@background
def assign_running_status(mail_id):
    mail_item = Mail.objects.get(pk=mail_id)
    mail_item.status = 'запущена'
    mail_item.save()


@background
def assign_done_status(mail_id):
    mail_item = Mail.objects.get(pk=mail_id)
    mail_item.status = 'завершена'
    mail_item.save()
