# Generated by Django 5.1.4 on 2024-12-29 00:44

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuario', '0002_ong_created_at_ong_updated_at'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ong',
            name='status',
            field=models.CharField(choices=[('Pendente', 'Pendente'), ('Em análise', 'Em análise'), ('Ativa', 'Ativa'), ('Inativa', 'Inativa')], default='', max_length=50),
        ),
    ]