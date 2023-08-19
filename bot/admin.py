from django.contrib import admin

from bot.models import BotUser, Measurement


@admin.register(BotUser)
class BotUserAdmin(admin.ModelAdmin):
    pass


@admin.register(Measurement)
class MeasurementAdmin(admin.ModelAdmin):
    pass
