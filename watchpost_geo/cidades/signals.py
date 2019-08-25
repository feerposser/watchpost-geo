from django.db.models.signals import post_save
from cidades.models import ModelCidade


def cidade(sender, instance, created, **kwargs):
    print(sender, instance, created, kwargs)
    print("SIGNAAAAALS")


post_save.connect(cidade, sender=ModelCidade)
