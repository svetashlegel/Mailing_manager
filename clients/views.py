from django.http import Http404
from django.views.generic import CreateView, DetailView, ListView, UpdateView, DeleteView
from django.urls import reverse
from clients.models import Client


class ClientCreateView(CreateView):
    model = Client
    fields = ('first_name', 'last_name', 'nick', 'email')

    def get_success_url(self):
        return reverse('clients:list')

    def form_valid(self, form):
        self.object = form.save()
        self.object.owner = self.request.user
        self.object.save()


class ClientUpdateView(UpdateView):
    model = Client
    fields = ('first_name', 'last_name', 'nick', 'email')

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("Вы не являетесь создателем данного клиента, у вас нет прав на его редактирование.")
        return self.object

    def get_success_url(self):
        return reverse('clients:view', args=[self.kwargs.get('pk')])


class ClientListView(ListView):
    model = Client

    def get_queryset(self):
        return super().get_queryset().filter(owner=self.request.user)


class ClientDetailView(DetailView):
    model = Client


class ClientDeleteView(DeleteView):
    model = Client

    def get_object(self, queryset=None):
        self.object = super().get_object(queryset)
        if self.object.owner != self.request.user:
            raise Http404("Вы не являетесь создателем данного клиента, у вас нет прав на его удаление.")
        return self.object

    def get_success_url(self):
        return reverse('clients:list')

