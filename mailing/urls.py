from django.urls import path
from django.views.decorators.cache import cache_page

from mailing.views import (index, contacts, MailCreateView, MailUpdateView, MailListView, MailDetailView, MailDeleteView,
                           MailLogfileDetailView, LogfileDetailView, toggle_activity)
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    path('', index, name='index'),
    path('contacts/', cache_page(60)(contacts), name='contacts'),
    path('list/', MailListView.as_view(), name='list'),
    path('view/<int:pk>', MailDetailView.as_view(), name='view'),
    path('create/', MailCreateView.as_view(), name='create'),
    path('edit/<int:pk>', MailUpdateView.as_view(), name='edit'),
    path('delete/<int:pk>', MailDeleteView.as_view(), name='delete'),
    path('logs/<int:pk>', MailLogfileDetailView.as_view(), name='log_list'),
    path('log_view/<int:pk>', LogfileDetailView.as_view(), name='log_view'),
    path('activity/<int:pk>', toggle_activity, name='toggle_activity'),
]
