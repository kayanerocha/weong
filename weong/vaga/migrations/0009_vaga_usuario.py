# Generated by Django 5.1.4 on 2025-01-23 00:05

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0009_alter_ong_table'),
        ('vaga', '0008_alter_endereco_table_alter_vaga_table'),
    ]

    operations = [
        migrations.AddField(
            model_name='vaga',
            name='usuario',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='usuario.ong'),
        ),
    ]
