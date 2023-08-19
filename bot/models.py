from django.db import models


class BotUser(models.Model):
    user = models.OneToOneField('auth.User', on_delete=models.CASCADE)
    email = models.EmailField(unique=True)
    tid = models.IntegerField(unique=True, verbose_name='Telegram User ID')


class Measurement(models.Model):
    user = models.ForeignKey('BotUser', on_delete=models.CASCADE)
    sys = models.PositiveIntegerField(blank=True, null=True, help_text='Systolic pressure')  # Systolic pressure in mmHg
    dia = models.PositiveIntegerField(blank=True, null=True, help_text='Diastolic pressure')  # Diastolic pressure in mmHg
    pls = models.PositiveIntegerField(blank=True, null=True, help_text='Pulse')  # Pulse rate in beats per minute
    dttm = models.DateTimeField(auto_now_add=True)  # Datetime of the measurement


class Schedule(models.Model):
    user = models.ForeignKey('BotUser', on_delete=models.CASCADE)
    time = models.TimeField()
    chat = models.IntegerField(verbose_name="Chat ID ~ User ID")

