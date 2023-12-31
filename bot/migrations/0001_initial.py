# Generated by Django 4.2.4 on 2023-08-19 15:20

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='BotUser',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('tid', models.IntegerField(unique=True, verbose_name='Telegram User ID')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Measurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('sys', models.PositiveIntegerField(blank=True, help_text='Systolic pressure', null=True)),
                ('dia', models.PositiveIntegerField(blank=True, help_text='Diastolic pressure', null=True)),
                ('pls', models.PositiveIntegerField(blank=True, help_text='Pulse', null=True)),
                ('dttm', models.DateTimeField(auto_now_add=True)),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='bot.botuser')),
            ],
        ),
    ]
