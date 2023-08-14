from django.urls import path

#from mailing.views import
from mailing.apps import MailingConfig

app_name = MailingConfig.name

urlpatterns = [
    #path('', ProductListView.as_view(), name='home'),
    #path('contacts/', contacts, name='contacts'),
    #path('view/<int:pk>', ProductDetailView.as_view(), name='view'),
    #path('create/', ProductCreateView.as_view(), name='create'),
    #path('edit/<int:pk>', ProductUpdateView.as_view(), name='edit'),
    #path('delete/<int:pk>', ProductDeleteView.as_view(), name='delete'),
]