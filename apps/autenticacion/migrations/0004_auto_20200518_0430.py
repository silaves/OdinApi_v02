# Generated by Django 3.0.4 on 2020-05-18 08:30

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0003_auto_20200518_0402'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='usuario',
            name='horario',
        ),
        migrations.AddField(
            model_name='horario',
            name='usuario',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL),
            preserve_default=False,
        ),
    ]
