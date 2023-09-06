from django import forms
from clients.models import Client
from mailing.forms import StyleFormMixin


class ClientForm(StyleFormMixin, forms.ModelForm):

    class Meta:
        model = Client
        fields = ('first_name', 'last_name', 'nick', 'email')
