from django.db import models

import mailing.models


NULLABLE = {'blank': True, 'null': True}


class Client(models.Model):
    first_name = models.CharField(max_length=150, verbose_name='имя')
    last_name = models.CharField(max_length=150, verbose_name='фамилия')
    nick = models.CharField(max_length=150, verbose_name='никнейм', unique=True)
    email = models.EmailField(verbose_name='почта')

    mails = models.ManyToManyField('mailing.Mail', through="Enrollment")

    def __str__(self):
        return f'{self.nick} ({self.email})'

    class Meta:
        verbose_name = 'клиент'
        verbose_name_plural = 'клиенты'


class Enrollment(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE, verbose_name='клиент')
    mail = models.ForeignKey('mailing.Mail', on_delete=models.CASCADE, verbose_name='письмо')

