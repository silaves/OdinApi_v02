# Generated by Django 3.0.4 on 2020-05-13 21:58

import apps.articulos.validators
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Articulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=50)),
                ('descripcion', models.CharField(blank=True, max_length=255)),
                ('precio', models.DecimalField(decimal_places=1, max_digits=7)),
                ('estado', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'verbose_name': 'articulo',
                'verbose_name_plural': 'articulos',
                'db_table': 'ARTICULO',
            },
        ),
        migrations.CreateModel(
            name='CategoriaArticulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100, unique=True)),
                ('codigo', models.CharField(max_length=20, unique=True)),
                ('estado', models.BooleanField(default=True)),
            ],
            options={
                'verbose_name': 'categoria articulo',
                'verbose_name_plural': 'categorias articulo',
                'db_table': 'CATEGORIA_ARTICULO',
            },
        ),
        migrations.CreateModel(
            name='ChatArticulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'chat articulo',
                'verbose_name_plural': 'chat articulos',
                'db_table': 'CHAT_ARTICULO',
            },
        ),
        migrations.CreateModel(
            name='Detalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('label', models.CharField(max_length=30)),
                ('valor', models.CharField(max_length=50)),
                ('estado', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'verbose_name': 'detalle',
                'verbose_name_plural': 'detalles',
                'db_table': 'DETALLE',
            },
        ),
        migrations.CreateModel(
            name='Favorito',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'favorito',
                'verbose_name_plural': 'favoritos',
                'db_table': 'FAVORITO',
            },
        ),
        migrations.CreateModel(
            name='FotoArticulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(blank=True, default='articulos/articulos/no-img.jpg', help_text='El tamaño maximo para las fotos es 3 Megas', null=True, upload_to='articulos/articulos/', validators=[apps.articulos.validators.tamaño_del_archivo])),
            ],
            options={
                'verbose_name': 'foto articulo',
                'verbose_name_plural': 'fotos articulos',
                'db_table': 'FOTO_ARTICULO',
            },
        ),
        migrations.CreateModel(
            name='FotoTienda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('foto', models.ImageField(help_text='El tamaño maximo para las fotos es 3 Megas', upload_to='articulos/tiendas/', validators=[apps.articulos.validators.tamaño_del_archivo])),
            ],
            options={
                'verbose_name': 'foto tienda',
                'verbose_name_plural': 'fotos tienda',
                'db_table': 'FOTO_TIENDA',
            },
        ),
        migrations.CreateModel(
            name='MensajeChat',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_propietario', models.IntegerField()),
                ('mensaje', models.TextField()),
                ('fecha', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'mensaje',
                'verbose_name_plural': 'mensajes',
                'db_table': 'MENSAJE_CHAT',
            },
        ),
        migrations.CreateModel(
            name='SubCategoriaArticulo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'verbose_name': 'sub categoria - articulo',
                'verbose_name_plural': 'sub categorias - articulo',
                'db_table': 'SUB_CATEGORIA_ARTICULO',
            },
        ),
        migrations.CreateModel(
            name='SubDetalle',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('valor', models.CharField(max_length=30)),
                ('estado', models.BooleanField(blank=True, default=True)),
            ],
            options={
                'verbose_name': 'sub detalle',
                'verbose_name_plural': 'sub detalles',
                'db_table': 'SUB_DETALLE',
            },
        ),
        migrations.CreateModel(
            name='Tienda',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('telefono', models.IntegerField()),
                ('direccion', models.CharField(max_length=255)),
                ('hora_inicio', models.TimeField(blank=True, default='09:00:00')),
                ('hora_fin', models.TimeField(blank=True, default='15:00:00')),
            ],
            options={
                'verbose_name': 'tienda',
                'verbose_name_plural': 'tiendas',
                'db_table': 'TIENDA',
            },
        ),
    ]
