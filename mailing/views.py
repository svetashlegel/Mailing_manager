import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse
from mailing.models import Mail, Logfile
from clients.models import Client
from blog.models import Article
from mailing.tasks import send_newsletter, assign_running_status, assign_done_status
from mailing.funcs import revert_command
from background_task.models import TaskManager, Task
from django.http import Http404

from users.models import User


def index(request):
    context_data = {
        'mailing_all': Mail.objects.count(),
        'mailing_active': Mail.objects.filter(status='запущена').count(),
        'clients': Client.objects.count(),
        'last_articles': Article.objects.all().order_by('-id')[:3]
    }
    return render(request, 'mailing/main_page.html', context=context_data)


def contacts(request):
    context_data = {
        'manager': User.objects.filter(groups__name='Manager')[0],
        'content_manager': User.objects.filter(groups__name='Content_manager')[0]
    }
    return render(request, 'mailing/contacts.html', context=context_data)


class MailCreateView(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    model = Mail
    fields = ('title', 'content', 'sending_time', 'sending_period', 'start_date', 'end_date', 'clients')
    permission_required = 'mailing.add_mail'

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

        obj.owner = self.request.user
        obj.save()

        task_name = 'mailing.tasks.send_newsletter'
        task_params = [[92], {}]
        hash = Task.objects.all()
        for h in hash:
            print(h.task_params)
        print(hash)
        print('jk')

        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mail
    fields = ('title', 'content', 'clients')
    permission_required = 'mailing.change_mail'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("Вы не являетесь создателем данной рассылки, у вас нет прав на её редактирование.")
        return self.object

    def get_success_url(self):
        return reverse('mailing:view', args=[self.kwargs.get('pk')])


class MailListView(LoginRequiredMixin, PermissionRequiredMixin, ListView):
    model = Mail
    permission_required = 'mailing.view_mail'

    def get_queryset(self):
        queryset = super().get_queryset()
        if not self.request.user.is_staff:
            queryset = queryset.filter(owner=self.request.user)
        return queryset


class MailDetailView(LoginRequiredMixin, PermissionRequiredMixin, DetailView):
    model = Mail
    permission_required = 'mailing.view_mail'


class MailDeleteView(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Mail
    permission_required = 'mailing.delete_mail'

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("Вы не являетесь создателем данной рассылки, у вас нет прав на её удаление.")
        return self.object

    def get_success_url(self):
        return reverse('mailing:list')


class MailLogfileDetailView(DetailView):
    model = Mail
    template_name = 'mailing/logfile_list.html'


class LogfileDetailView(DetailView):
    model = Logfile


class TaskListView(PermissionRequiredMixin, ListView):
    model = Task
    permission_required = 'background_task.view_task'


class TaskDeleteView(PermissionRequiredMixin, DeleteView):
    model = Task
    permission_required = 'background_task.delete_task'

    def get_success_url(self):
        return reverse('mailing:tasklist')
