from django.db import models
from django.utils.timezone import now
import clients.models


NULLABLE = {'blank': True, 'null': True}


class Period(models.Model):
    period = models.CharField(max_length=150, verbose_name='периодичность')
    description = models.TextField(verbose_name='содержание')

    def __str__(self):
        return f'{self.period}'

    class Meta:
        verbose_name = 'период'
        verbose_name_plural = 'периоды'


class Mail(models.Model):
    title = models.CharField(max_length=150, verbose_name='тема письма')
    content = models.TextField(verbose_name='тело письма')
    sending_time = models.TimeField(default='12:00', verbose_name='время рассылки')
    sending_period = models.ForeignKey(Period, on_delete=models.CASCADE, verbose_name='период')
    status = models.CharField(max_length=150, default='создана', verbose_name='статус рассылки')
    start_date = models.DateField(default=now, verbose_name='начало рассылки')
    end_date = models.DateField(**NULLABLE, verbose_name='окончание рассылки')

    clients = models.ManyToManyField(clients.models.Client, through="clients.Enrollment")

    def __str__(self):
        return f'{self.title}'

    class Meta:
        verbose_name = 'письмо'
        verbose_name_plural = 'письма'


class Logfile(models.Model):
    date = models.DateTimeField(verbose_name='дата и время последней попытки')
    is_success = models.BooleanField(verbose_name='статус: успешно')
    mail = models.ForeignKey(Mail, on_delete=models.CASCADE, verbose_name='рассылка')

    def __str__(self):
        return f'Лог {self.pk}'

    class Meta:
        verbose_name = 'лог'
        verbose_name_plural = 'логи'
