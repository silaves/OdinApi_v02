# Generated by Django 3.0.4 on 2020-05-08 02:51

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('empresa', '0002_pedido_repartidor'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pedido',
            name='repartidor',
            field=models.ForeignKey(blank=True, default=None, null=True, on_delete=django.db.models.deletion.PROTECT, related_name='repartidor', to=settings.AUTH_USER_MODEL),
        ),
    ]