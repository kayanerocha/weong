# Generated by Django 5.1.4 on 2024-12-29 01:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0003_alter_ong_status'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ong',
            name='site',
            field=models.URLField(blank=True, max_length=255, null=True),
        ),
    ]