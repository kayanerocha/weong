# Generated by Django 5.1.4 on 2024-12-29 01:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0005_ong_email'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='ong',
            name='email',
        ),
    ]
