# Generated by Django 5.0.9 on 2025-05-05 18:39

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('NexworkApp', '0009_usuario_ocupacion'),
    ]

    operations = [
        migrations.CreateModel(
            name='ExperienciaLaboral',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('puesto', models.CharField(max_length=100)),
                ('empresa', models.CharField(max_length=100)),
                ('fecha_inicio', models.DateField()),
                ('fecha_fin', models.DateField(blank=True, null=True)),
                ('descripcion', models.TextField(blank=True)),
                ('tecnologias', models.CharField(blank=True, max_length=255)),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='experiencias', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'ordering': ['-fecha_inicio'],
            },
        ),
    ]
