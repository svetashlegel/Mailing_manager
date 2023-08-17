from django.conf import settings
from django.core.mail import send_mail
from background_task import background

from mailing.models import Mail


@background
def send_newsletter(mail_id):
    mail_item = Mail.objects.get(pk=mail_id)
    send_mail(
        mail_item.title,
        mail_item.content,
        settings.EMAIL_HOST_USER,
        ['shlegel.s@me.com']
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
