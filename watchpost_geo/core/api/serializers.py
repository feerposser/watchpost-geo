from rest_framework.serializers import ModelSerializer

from cidades.models import ModelCidade


class SerializerCidade(ModelSerializer):

    class Meta:
        model = ModelCidade
        fields = ['nome', 'bounds_northeast_lat', 'bounds_northeast_lng', 'bounds_southwest_lat',
                  'bounds_southwest_lng', 'latitude', 'longitude', 'distancia_maxima', 'endereco']
