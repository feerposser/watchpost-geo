# Generated by Django 2.2.3 on 2019-07-12 21:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('bairros', '0004_auto_20190712_1815'),
    ]

    operations = [
        migrations.RenameField(
            model_name='modelbairro',
            old_name='distancia_maxima_km',
            new_name='distancia_maxima',
        ),
    ]
