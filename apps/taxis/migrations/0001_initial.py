# Generated by Django 3.0.4 on 2020-05-13 21:58

import apps.taxis.validators
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
            name='Movil',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('placa', models.CharField(max_length=10, unique=True)),
                ('color', models.CharField(max_length=30)),
                ('modelo', models.CharField(max_length=50)),
                ('foto', models.ImageField(blank=True, default='moviles/no-img.jpg', help_text='El tamaño maximo para las fotos es 3 Megas', null=True, upload_to='moviles/', validators=[apps.taxis.validators.tamaño_del_archivo])),
                ('taxista', models.ForeignKey(on_delete=django.db.models.deletion.PROTECT, related_name='movil', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'movil',
                'verbose_name_plural': 'moviles',
                'db_table': 'MOVIL',
            },
        ),
    ]
