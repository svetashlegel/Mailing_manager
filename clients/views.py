from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse
from clients.models import Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'nick', 'email')

    def get_success_url(self):
        return reverse('clients:list')


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'nick', 'email')

    def get_success_url(self):
        return reverse('clients:view', args=[self.kwargs.get('pk')])


class ClientListView(ListView):
    model = Client


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client

    def get_success_url(self):
        return reverse('clients:list')

