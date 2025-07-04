# Generated by Django 5.1.7 on 2025-06-15 21:13

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFlexi', '0011_alter_cargaflexirampla_fecha_armado_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='imagencarga',
            name='nombre',
            field=models.CharField(blank=True, max_length=100),
        ),
        migrations.AlterField(
            model_name='imagencarga',
            name='carga_flexirampla',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppFlexi.cargaflexirampla'),
        ),
        migrations.AlterField(
            model_name='imagencarga',
            name='carga_flexitank',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='AppFlexi.cargaflexitank'),
        ),
        migrations.AlterField(
            model_name='imagencarga',
            name='imagen',
            field=models.ImageField(upload_to='imagenes/'),
        ),
    ]
