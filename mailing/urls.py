from django.urls import path

from mailing.views import (MailCreateView, MailUpdateView, MailListView, MailDetailView, MailDeleteView,
                           MailLogfileDetailView, LogfileDetailView, TaskListView, TaskDeleteView)
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', MailListView.as_view(), name='list'),
    #path('contacts/', contacts, name='contacts'),
    path('view/<int:pk>', MailDetailView.as_view(), name='view'),
    path('create/', MailCreateView.as_view(), name='create'),
    path('edit/<int:pk>', MailUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailDeleteView.as_view(), name='delete'),
    path('logs/<int:pk>', MailLogfileDetailView.as_view(), name='log_list'),
    path('log_view/<int:pk>', LogfileDetailView.as_view(), name='log_view'),

    path('deletetask/<int:pk>', TaskDeleteView.as_view(), name='deletetask'),
    path('tasklist', TaskListView.as_view(), name='tasklist'),
]
