import datetime
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse
from mailing.models import Mail
from mailing.tasks import send_newsletter, assign_running_status, assign_done_status
from mailing.funcs import revert_command


class MailCreateView(CreateView):
    model = Mail
    fields = ('title', 'content', 'sending_time', 'sending_period', 'start_date', 'end_date')

    def get_success_url(self):
        return reverse('mailing:list')

    def form_valid(self, form):
        obj = form.save()

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

        return super().form_valid(form)


class MailUpdateView(UpdateView):
    model = Mail
    fields = ('title', 'content', 'sending_time', 'sending_period')

    def get_success_url(self):
        return reverse('mailing:view', args=[self.kwargs.get('pk')])


class MailListView(ListView):
    model = Mail


class MailDetailView(DetailView):
    model = Mail


class MailDeleteView(DeleteView):
    model = Mail

    def get_success_url(self):
        return reverse('mailing:list')
