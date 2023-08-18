from django.contrib import admin
from mailing.models import Period, Mail, Logfile


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('period', 'description')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('title', 'sending_period', 'status')


@admin.register(Logfile)
class LogfileAdmin(admin.ModelAdmin):
    list_display = ('date', 'is_success', 'mail')
