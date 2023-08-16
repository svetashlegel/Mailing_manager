from django.contrib import admin
from mailing.models import Period, Mail


@admin.register(Period)
class PeriodAdmin(admin.ModelAdmin):
    list_display = ('period', 'description')


@admin.register(Mail)
class MailAdmin(admin.ModelAdmin):
    list_display = ('title', 'sending_period', 'status')
