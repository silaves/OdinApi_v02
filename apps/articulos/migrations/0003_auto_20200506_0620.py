# Generated by Django 3.0.4 on 2020-05-06 10:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('articulos', '0002_auto_20200502_1934'),
    ]

    operations = [
        migrations.AlterField(
            model_name='subcategoriaarticulo',
            name='padre',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='sub_categorias', to='articulos.CategoriaArticulo'),
        ),
    ]
