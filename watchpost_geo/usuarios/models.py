from django.db import models
from django.contrib.auth.models import User


class ModelRequestByUser(models.Model):

    user = models.OneToOneField(User, on_delete=models.SET("Undefined User"))
    input_cidade = models.CharField(max_length=250)
    input_bairro = models.CharField(max_length=250)
    input_rua = models.CharField(max_length=250, null=True, blank=True)
    input_numero = models.CharField(max_length=250, null=True, blank=True)
    input_estado = models.CharField(max_length=250)
    confidence = models.CharField(max_length=250, null=True, blank=True)
    search_address = models.CharField(max_length=250, null=True, blank=True)
    geocode_lat = models.FloatField(null=True, blank=True)
    geocode_lng = models.FloatField(null=True, blank=True)
    errors = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)


class ModelCountRequests(models.Model):

    counter = models.IntegerField()
    updated_at = models.DateTimeField(auto_now_add=True)