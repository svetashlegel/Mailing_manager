from django.urls import path

from clients.views import ClientCreateView, ClientUpdateView, ClientListView, ClientDetailView, ClientDeleteView
from clients.apps import ClientsConfig

app_name = ClientsConfig.name

urlpatterns = [
    path('list/', ClientListView.as_view(), name='list'),
    path('view/<int:pk>', ClientDetailView.as_view(), name='view'),
    path('create/', ClientCreateView.as_view(), name='create'),
    path('edit/<int:pk>', ClientUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', ClientDeleteView.as_view(), name='delete'),
]
