# Generated by Django 2.2.3 on 2019-08-24 19:35

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('usuarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='modelrequestbyuser',
            name='user',
            field=models.OneToOneField(on_delete=models.SET('Undefined User'), to=settings.AUTH_USER_MODEL),
        ),
    ]