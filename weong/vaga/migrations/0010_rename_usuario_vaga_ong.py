# Generated by Django 5.1.4 on 2025-01-23 00:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaga', '0009_vaga_usuario'),
    ]

    operations = [
        migrations.RenameField(
            model_name='vaga',
            old_name='usuario',
            new_name='ong',
        ),
    ]
