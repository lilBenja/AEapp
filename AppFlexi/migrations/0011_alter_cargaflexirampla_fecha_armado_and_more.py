# Generated by Django 5.1.7 on 2025-06-13 23:48

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFlexi', '0010_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargaflexirampla',
            name='fecha_armado',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.AlterField(
            model_name='cargaflexitank',
            name='fecha_armado',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
        migrations.DeleteModel(
            name='CustomUser',
        ),
    ]
