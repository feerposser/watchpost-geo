from .models import ModelBlackList
from cidades.models import ModelCidade
from alg_utils.watchpost_exceptions import CreateBlackListError


class ManageBlackList:

    @staticmethod
    def create_or_retrieve_blacklist(city, neighborhood, **kwargs):
        try:
            assert isinstance(city, ModelCidade), "city deve ser um obj Modelcidade e não '%s'" % type(city)
            if not ModelBlackList.objects.filter(cidade=city, bairro=neighborhood).exists():
                blacklist = ModelBlackList()
                blacklist.cidade = city
                blacklist.bairro = neighborhood

                if "endereco_completo" in kwargs:
                    blacklist.endereco_completo = kwargs['endereco_completo']
                if "bounds_northeast_lat" in kwargs:
                    blacklist.bounds_northeast_lat = kwargs['bounds_northeast_lat']
                if "bounds_northeast_lng" in kwargs:
                    blacklist.bounds_northeast_lng = kwargs['bounds_northeast_lng']
                if "bounds_southwest_lat" in kwargs:
                    blacklist.bounds_southwest_lat = kwargs['bounds_southwest_lat']
                if "bounds_southwest_lng" in kwargs:
                    blacklist.bounds_southwest_lng = kwargs['bounds_southwest_lng']
                if "latitude" in kwargs:
                    blacklist.latitude = kwargs['latitude']
                if "longitude" in kwargs:
                    blacklist.longitude = kwargs['longitude']
                if "status" in kwargs:
                    blacklist.status = kwargs['status']
                if "usuario" in kwargs:
                    blacklist.usuario = kwargs['usuario']

                blacklist.save()

                return blacklist
            else:
                return ModelBlackList.objects.get(cidade=city, bairro=neighborhood)
        except AssertionError as a:
            print(811, a.__repr__())
            raise CreateBlackListError(811, a.__repr__())
        except Exception as e:
            print(812, e.__repr__())
            raise CreateBlackListError(812, e.__repr__())
