# Generated by Django 3.0.4 on 2020-05-08 07:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresa', '0008_auto_20200507_2318'),
    ]

    operations = [
        migrations.RenameField(
            model_name='pedido',
            old_name='direccion',
            new_name='ubicacion',
        ),
        migrations.AddField(
            model_name='sucursal',
            name='ubicacion',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]