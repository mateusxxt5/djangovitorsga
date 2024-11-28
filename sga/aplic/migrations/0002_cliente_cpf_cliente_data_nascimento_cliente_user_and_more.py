# Generated by Django 4.2.16 on 2024-11-28 02:47

from django.conf import settings
import django.core.validators
from django.db import migrations, models
import django.db.models.deletion
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('aplic', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='cliente',
            name='cpf',
            field=models.CharField(default='000.000.000-00', max_length=14, unique=True, validators=[django.core.validators.RegexValidator(message='CPF deve estar no formato XXX.XXX.XXX-XX', regex='^\\d{3}\\.\\d{3}\\.\\d{3}-\\d{2}$')]),
        ),
        migrations.AddField(
            model_name='cliente',
            name='data_nascimento',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.AddField(
            model_name='cliente',
            name='user',
            field=models.OneToOneField(default=1, on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='cliente',
            name='endereco',
            field=models.TextField(blank=True),
        ),
    ]
