from django.urls import path

#from clients.views import
from clients.apps import ClientsConfig

app_name = ClientsConfig.name

urlpatterns = [
    #path('', MailListView.as_view(), name='list'),
    #path('contacts/', contacts, name='contacts'),
    #path('view/<int:pk>', MailDetailView.as_view(), name='view'),
    #path('create/', MailCreateView.as_view(), name='create'),
    #path('edit/<int:pk>', MailUpdateView.as_view(), name='edit'),
    #path('delete/<int:pk>', MailDeleteView.as_view(), name='delete'),
]
