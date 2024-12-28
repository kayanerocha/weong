# Generated by Django 5.1.4 on 2024-12-28 00:25

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('vaga', '0006_alter_endereco_complemento'),
    ]

    operations = [
        migrations.AddField(
            model_name='endereco',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='endereco',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
    ]