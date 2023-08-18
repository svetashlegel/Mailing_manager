from django.contrib import admin
from clients.models import Client, Enrollment


@admin.register(Client)
class ClientAdmin(admin.ModelAdmin):
    list_display = ('nick', 'email')


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ('client', 'mail')
