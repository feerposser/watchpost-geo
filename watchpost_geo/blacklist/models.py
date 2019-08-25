from django.db import models

from cidades.models import ModelCidade


class ModelBlackList(models.Model):
    STATUS_CHOICES = (
        ('A', 'ATIVO'),
        ('R', 'RESOLVIDO'),
    )

    cidade = models.ForeignKey(ModelCidade, on_delete=models.CASCADE)
    bairro = models.CharField(max_length=250)
    endereco_completo = models.CharField(max_length=250, blank=True, null=True)
    bounds_northeast_lat = models.FloatField(blank=True, null=True)
    bounds_northeast_lng = models.FloatField(blank=True, null=True)
    bounds_southwest_lat = models.FloatField(blank=True, null=True)
    bounds_southwest_lng = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    status = models.CharField(max_length=100, choices=STATUS_CHOICES, default='A')
    usuario = models.CharField(max_length=100, default="Thomas Shelby")
    criacao = models.DateTimeField(auto_now_add=True)
    alteracao = models.DateTimeField(auto_now=True)

    def __str__(self):
        return str(self.cidade) + " - " + self.bairro

    class Meta:
        db_table = 'blacklist'
        verbose_name = 'Blacklist'
        verbose_name_plural = 'Blacklists'
