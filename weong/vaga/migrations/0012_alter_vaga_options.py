# Generated by Django 5.1.4 on 2025-02-08 01:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('vaga', '0011_alter_vaga_endereco'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='vaga',
            options={'permissions': (('criar_vaga', 'Criar vaga.'),)},
        ),
    ]
