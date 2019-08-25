import googlemaps
from geopy import distance
from django.core.exceptions import ObjectDoesNotExist

from .models import ModelCidade


class ManageCity:

    google_maps_city_types = ('political', 'administrative_area_level_2')

    def __init__(self, name):
        try:
            assert str(name).replace(" ", "") != "", "parâmetro name inválido"
            self.city_data = ModelCidade.objects.get(nome__iexact=name)
        except ObjectDoesNotExist as o:
            print('Não encontrado:', o.__repr__())
            self.city_data = None
        except AssertionError as a:
            print('problame de validação', a.__repr__())
            self.city_data = None
        finally:
            self.city_name = name

    def city_exists(self, name=""):
        try:
            if self.city_data:
                return self.city_data
            else:
                assert name.replace(" ", "") != "", "parâmetro name inválido"
                return ModelCidade.objects.get(nome__iexact=name)
        except ObjectDoesNotExist as o:
            print(o)
            return False
        except Exception as e:
            print(e)
            return False

    def get_city_bounds(self):
        return {
            'northeast': {
                 'lat': self.city_data.bounds_northeast_lat,
                 'lng': self.city_data.bounds_northeast_lng
            },
            'southwest': {
                'lat': self.city_data.bounds_southwest_lat,
                'lng': self.city_data.bounds_southwest_lng
            }
        }

    def get_city_data(self):
        return self.city_data

    def get_city_center(self):
        return {
            'lat': self.city_data.latitude,
            'lng': self.city_data.longitude
        }

    def get_city_max_distance(self):
        return self.city_data.distancia_maxima

    def get_distance_to_city_center(self, point_incident, metric='km'):
        """
        Retorna a distância do ponto de latitude e longitude do incidente com a distância do centro da cidade em km
        :param point_incident: (lat, lng)
        :param metric: str com o tipo de distância (metros ou km)
        :return: float
        """
        try:
            assert metric == "km" or metric == "meters", \
                "Parâmetro metric deve ser 'km' ou 'meters' e não '%s'" % metric
            # Converte os valores para (lat,lng)
            point_incident = googlemaps.convert.normalize_lat_lng(point_incident)
            point_city = googlemaps.convert.normalize_lat_lng(self.get_city_center())
            if metric == 'km':
                return distance.distance(point_incident, point_city).km
            elif metric == 'meters':
                return distance.distance(point_incident, point_city).meters
        except AssertionError as a:
            print(411, a.__repr__())
            raise AssertionError(411, a.args)
        except Exception as e:
            print(412, repr(e))
            raise Exception(412, e.args)

    def is_inside_city(self, location):
        """
        Analisa se um ponto de latitude e longidude está dentro da cidade
        :param location: estrutura geocode completa ou dict ['geometry']['location']
        :return: False se estiver fora da cidade, True se estiver dentro da cidade
        """
        try:
            assert isinstance(location, (tuple, dict)), "parâmetro city deve ser tupla ou dicionário"

            city_bounds = self.get_city_bounds()
            if 'geometry' in location:
                location = location['geometry']['location']

            if isinstance(location, dict):
                if location['lat'] > city_bounds['northeast']['lat'] or \
                        location['lat'] < city_bounds['southwest']['lat'] or \
                        location['lng'] > city_bounds['northeast']['lng'] or \
                        location['lng'] < city_bounds['southwest']['lng']:
                    return False
            else:
                raise AssertionError("Análise por tupla indisponível nesta versão.")
            return True
        except AssertionError as a:
            print(421, a.__repr__())
            return False
        except Exception as e:
            print(422, e.__repr__())
            return False

    @staticmethod
    def get_city_model(name):
        try:
            assert str(name).replace(" ", "") != "", "parâmetro name inválido"
            return ModelCidade.objects.get(nome__icontains=name)
        except ObjectDoesNotExist as o:
            print(431, o.__repr__())
            return False
        except Exception as e:
            print(432, e.__repr__())
            return False
