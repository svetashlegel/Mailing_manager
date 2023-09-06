from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render, redirect
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse
from mailing.models import Mail, Logfile
from clients.models import Client
from blog.models import Article
from users.models import User
from background_task.models import Task
from mailing.forms import MailCreateForm, MailUpdateForm
from django.http import Http404
from mailing.services import create_mailing, resume_mailing


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
    form_class = MailCreateForm
    permission_required = 'mailing.add_mail'

    def get_success_url(self):
        return reverse('mailing:list')

    def form_valid(self, form):
        obj = form.save()
        create_mailing(obj)
        obj.owner = self.request.user
        obj.save()

        return super().form_valid(form)


class MailUpdateView(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    model = Mail
    form_class = MailUpdateForm
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


def toggle_activity(request, pk):
    mail = Mail.objects.get(pk=pk)
    print(f'mail.pk {mail.pk}')
    pk = str(mail.pk)
    print(f'str.pk {pk}')
    count = len(pk)
    print(f'кол-во мест {count}')
    if mail.is_going:
        mail.is_going = False
        status_tasks = Task.objects.filter(task_name='mailing.tasks.assign_done_status')
        for task in status_tasks:
            params = task.params
            params = params()[0][0]
            print(params)
            if params == mail.pk:
                mail_status_task = task
                print(mail_status_task)
                mail_status_task.delete()

        send_tasks = Task.objects.filter(task_name='mailing.tasks.send_newsletter')
        for task in send_tasks:
            params = task.params
            params = params()[0][0]
            print(params)
            if params == mail.pk:
                mail_status_task = task
                print(mail_status_task)
                mail_status_task.delete()
    else:
        mail.is_going = True
        resume_mailing(mail)
    mail.save()
    return redirect(reverse('mailing:list'))

