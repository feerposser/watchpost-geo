# Generated by Django 2.2.3 on 2019-07-15 14:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cidades', '0002_auto_20190712_1816'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelcidade',
            name='distancia_maxima',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
