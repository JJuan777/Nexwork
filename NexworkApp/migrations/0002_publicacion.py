# Generated by Django 5.0.9 on 2025-04-23 18:24

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NexworkApp', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Publicacion',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('descripcion', models.TextField(verbose_name='Descripción')),
                ('imagen', models.BinaryField(blank=True, null=True)),
                ('archivo', models.BinaryField(blank=True, null=True)),
                ('nombre_archivo', models.CharField(blank=True, max_length=255, null=True)),
                ('fecha_creacion', models.DateTimeField(auto_now_add=True)),
                ('fecha_actualizacion', models.DateTimeField(auto_now=True)),
                ('es_publico', models.BooleanField(default=True)),
                ('autor', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='publicaciones', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_creacion'],
            },
        ),
    ]
