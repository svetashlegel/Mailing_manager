import datetime
from mailing.tasks import send_newsletter, assign_running_status, assign_done_status
from mailing.funcs import revert_command


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
