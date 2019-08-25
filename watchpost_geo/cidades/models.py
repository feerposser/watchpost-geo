from django.db import models

from alg_utils.utils import max_distance


class ModelCidade(models.Model):
    nome = models.CharField(max_length=100)
    bounds_northeast_lat = models.FloatField()
    bounds_northeast_lng = models.FloatField()
    bounds_southwest_lat = models.FloatField()
    bounds_southwest_lng = models.FloatField()
    latitude = models.FloatField()
    longitude = models.FloatField()
    distancia_maxima = models.FloatField(null=True, blank=True)
    endereco = models.CharField(max_length=200, blank=True, null=True)
    criacao = models.DateTimeField(auto_now_add=True)
    alteracao = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = 'cidades'
        verbose_name = 'Informação da cidade'
        verbose_name_plural = 'Informações das cidades'

    def __str__(self):
        return self.nome

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if self.bounds_northeast_lat and self.bounds_northeast_lng and \
                self.bounds_southwest_lat and self.bounds_southwest_lng:

            self.distancia_maxima = round(max_distance(self.bounds_northeast_lat,
                                                       self.bounds_northeast_lng,
                                                       self.bounds_southwest_lat,
                                                       self.bounds_southwest_lng) / 2,
                                          3)
        super().save()
