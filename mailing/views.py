from django.shortcuts import render
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse
from mailing.models import Mail


class MailCreateView(CreateView):
    model = Mail
    fields = ('title', 'content', 'sending_time', 'sending_period')

    def get_success_url(self):
        return reverse('mailing:list')


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
