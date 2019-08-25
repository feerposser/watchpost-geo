from django.db import models

from alg_utils.utils import max_distance
from cidades.models import ModelCidade


class ModelBairro(models.Model):
    MODELBAIRRO_STATUS_CHOICES = (
        ("A", "ATIVO"),
        ("D", "DESATIVADO"),
        ("I", "INDEFINIDO")
    )

    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(ModelCidade, on_delete=models.CASCADE)
    bounds_northeast_lat = models.FloatField(blank=True, null=True)
    bounds_northeast_lng = models.FloatField(blank=True, null=True)
    bounds_southwest_lat = models.FloatField(blank=True, null=True)
    bounds_southwest_lng = models.FloatField(blank=True, null=True)
    latitude = models.FloatField(blank=True, null=True)
    longitude = models.FloatField(blank=True, null=True)
    endereco = models.CharField(max_length=150, blank=True, null=True)
    distancia_maxima = models.FloatField(null=True, blank=True)
    criacao = models.DateTimeField(auto_now_add=True)
    alteracao = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=1, choices=MODELBAIRRO_STATUS_CHOICES, default="A")

    class Meta:
        db_table = 'bairros'
        verbose_name = 'Informação do bairro'
        verbose_name_plural = 'Informações dos bairros'

    def __str__(self):
        return str(self.nome) + " - " + self.cidade.nome

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        """
        Antes de salvar verifica se os dados dos bounds são existentes. Se forem, os utilizará para analisar qual
        é a distância máxima aproximada para o bairro. Isso será utilizado para saber se um incidente está
        perto ou longe do centro do bairro para saber a confiabilidade do dado encontrado no geocode.
        A foórmula é a hipotenusa dividido por 2, dando assim a máxima distância de um local até o centro do bairro
        :param force_insert:
        :param force_update:
        :param using:
        :param update_fields:
        :return:
        """
        if self.bounds_northeast_lat and self.bounds_northeast_lng and \
                self.bounds_southwest_lat and self.bounds_southwest_lng:

            self.distancia_maxima = round(max_distance(self.bounds_northeast_lat,
                                                       self.bounds_northeast_lng,
                                                       self.bounds_southwest_lat,
                                                       self.bounds_southwest_lng) / 2,
                                          3)
        super().save()


class ModelBairroAuxiliar(models.Model):
    nome = models.CharField(max_length=100)
    cidade = models.ForeignKey(ModelCidade, on_delete=models.CASCADE)
    fk_bairro = models.ForeignKey(ModelBairro, on_delete=models.CASCADE)

    class Meta:
        db_table = 'informacao_bairros_auxiliar'
        verbose_name = 'Informação errada de bairro'
        verbose_name_plural = 'Informações erradas de bairros'

    def __str__(self):
        return self.nome + ' - ' + self.cidade.nome
