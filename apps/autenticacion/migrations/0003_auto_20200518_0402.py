# Generated by Django 3.0.4 on 2020-05-18 08:02

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('autenticacion', '0002_usuario_ciudad'),
    ]

    operations = [
        migrations.CreateModel(
            name='Horario',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('entrada', models.TimeField()),
                ('salida', models.TimeField()),
                ('estado', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'verbose_name': 'horario',
                'verbose_name_plural': 'horarios',
                'db_table': 'HORARIO',
            },
        ),
        migrations.AddField(
            model_name='usuario',
            name='horario',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.PROTECT, to='autenticacion.Horario'),
        ),
    ]