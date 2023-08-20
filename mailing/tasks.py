from django.conf import settings
from django.core.mail import send_mail
from background_task import background
from datetime import datetime

from mailing.models import Mail, Logfile


@background
def send_newsletter(mail_id):
    is_suc = True
    error = 'No errors'
    clients_list = []
    mail_item = Mail.objects.get(pk=mail_id)
    for client in mail_item.clients.all():
        clients_list.append(client.email)
    print(clients_list)
    print(mail_item)
    try:
        send_mail(
            mail_item.title,
            mail_item.content,
            settings.EMAIL_HOST_USER,
            clients_list,
            fail_silently=False
        )
    except Exception as err:
        print(f"Unexpected {err=}, {type(err)=}")
        is_suc = False
        error = f"Unexpected {err=}, {type(err)=}"
    finally:
        send_at = datetime.now()
        log = Logfile.objects.create(date=send_at, is_success=is_suc, mail_id=mail_item.pk,
                                     send_from=settings.EMAIL_HOST_USER, send_to=clients_list,
                                     mail_title=mail_item.title, mail_content=mail_item.content, error=error)
        log.save()



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
