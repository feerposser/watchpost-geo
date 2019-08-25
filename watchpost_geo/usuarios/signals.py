from django.db.models.signals import post_save
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from .models import ModelCountRequests, ModelRequestByUser


def create_token(sender, instance, created, **kwargs):
    if created:
        Token.objects.create(
            user=instance
        )


def counter_request(sender, instance, created, **kwargs):
    if created:
        counter = ModelCountRequests.objects.get(id=1)
        counter.counter += 1
        counter.save()


post_save.connect(create_token, sender=User)
post_save.connect(counter_request, sender=ModelRequestByUser)
