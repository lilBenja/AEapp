# Generated by Django 5.1.7 on 2025-04-01 00:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppFlexi', '0003_alter_empresa_nombre'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cargaflexirampla',
            name='empresa',
            field=models.CharField(choices=[('Tiba', 'Tiba'), ('Manuport', 'Manuport'), ('Hillebrand', 'Hillebrand'), ('DHL', 'DHL'), ('Belog', 'Belog'), ('Cacsa', 'Cacsa'), ('Otra', 'Otra empresa')], default='Otra', max_length=50),
        ),
        migrations.AlterField(
            model_name='cargaflexitank',
            name='empresa',
            field=models.CharField(choices=[('Tiba', 'Tiba'), ('Manuport', 'Manuport'), ('Hillebrand', 'Hillebrand'), ('DHL', 'DHL'), ('Belog', 'Belog'), ('Cacsa', 'Cacsa'), ('Otra', 'Otra empresa')], default='Otra', max_length=50),
        ),
    ]
