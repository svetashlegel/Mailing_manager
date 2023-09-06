import datetime
from mailing.tasks import send_newsletter, assign_running_status, assign_done_status
from mailing.funcs import revert_command
from background_task.models import Task


def create_mailing(obj):
    hour = obj.sending_time.hour - 3
    start = datetime.datetime(year=obj.start_date.year, month=obj.start_date.month, day=obj.start_date.day,
                              hour=hour, minute=obj.sending_time.minute,
                              second=obj.sending_time.second)
    end = datetime.datetime(year=obj.end_date.year, month=obj.end_date.month, day=obj.end_date.day,
                            hour=hour, minute=obj.sending_time.minute,
                            second=obj.sending_time.second)
    rep = revert_command(obj.sending_period.description)

    send_newsletter(obj.pk, schedule=start, repeat=rep, repeat_until=end)
    assign_running_status(obj.pk, schedule=start)
    assign_done_status(obj.pk, schedule=end)


def resume_mailing(mail):
    hour = mail.sending_time.hour - 3
    start = datetime.datetime(year=mail.start_date.year, month=mail.start_date.month, day=mail.start_date.day,
                              hour=hour, minute=mail.sending_time.minute,
                              second=mail.sending_time.second)
    end = datetime.datetime(year=mail.end_date.year, month=mail.end_date.month, day=mail.end_date.day,
                            hour=hour, minute=mail.sending_time.minute,
                            second=mail.sending_time.second)
    rep = revert_command(mail.sending_period.description)

    send_newsletter(mail.pk, schedule=start, repeat=rep, repeat_until=end)
    assign_done_status(mail.pk, schedule=end)


def delete_status_task(mail):
    status_tasks = Task.objects.filter(task_name='mailing.tasks.assign_done_status')
    for task in status_tasks:
        params = task.params
        params = params()[0][0]
        if params == mail.pk:
            mail_status_task = task
            mail_status_task.delete()


def delete_sending_task(mail):
    send_tasks = Task.objects.filter(task_name='mailing.tasks.send_newsletter')
    for task in send_tasks:
        params = task.params
        params = params()[0][0]
        if params == mail.pk:
            mail_status_task = task
            mail_status_task.delete()