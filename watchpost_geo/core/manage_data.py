import googlemaps

from bairros.manage_data import ManageNeighborhood
from cidades.manage_data import ManageCity
from blacklist.manage_data import ManageBlackList
from .report import Report
from alg_utils.watchpost_exceptions import GeocodeNotTrusted, NeighborhoodOrStreetNotSetup, GeocodeNotFound, \
    MaxDistanceNeighborhoodNotFound, CreateBlackListError


class ManageCoreBase(ManageCity, ManageNeighborhood):
    gmaps = googlemaps.Client(key='AIzaSyBYoU0ZrNNsAK-56cJBMK2LooCa5RtgqfQ')
    report = Report()
    formatted_address = ""  # endereço formatado para realizar a busca na API

    confidence_code = {"code": 0, "distance_neighborhood": ""}

    def __init__(self, neighborhood, city, user, state='RS'):
        ManageNeighborhood.__init__(self, neighborhood, city)
        ManageCity.__init__(self, city)
        self.state = state
        self.user = user

    def get_report(self):
        return self.report.report

    @staticmethod
    def get_lat_lng(data):
        """
        Pega a latitude e longitude
        :param data: dicionário retornado pela biblioteca python da API do Google Maps
        :return: {'lat': valor de latitude, 'lng': valor de longitude}
        """
        try:
            return data['geometry']['location']
        except Exception as e:
            raise Exception(221, e.args)

    @staticmethod
    def dict_to_bounds(neighborhood_model_obj):
        """
        transforma um dicionário simples em bounds para o googlemaps api
        :param neighborhood_model_obj: dict simples {'': ...., '':...}
        :return: bounds no formato dict
        """
        try:

            assert 'bounds_northeast_lat' in neighborhood_model_obj, "'bounds_northeast_lat' não presente"
            assert 'bounds_northeast_lng' in neighborhood_model_obj, "'bounds_northeast_lat' não presente"
            assert 'bounds_southwest_lat' in neighborhood_model_obj, "'bounds_northeast_lat' não presente"
            assert 'bounds_southwest_lng' in neighborhood_model_obj, "'bounds_northeast_lat' não presente"

            return {
                'northeast': {
                    'lat': neighborhood_model_obj['bounds_northeast_lat'],
                    'lng': neighborhood_model_obj['bounds_northeast_lng']
                },
                'southwest': {
                    'lat': neighborhood_model_obj['bounds_southwest_lat'],
                    'lng': neighborhood_model_obj['bounds_southwest_lng']
                }
            }
        except AssertionError as a:
            print(a.__repr__())
            raise AssertionError(221, a.args)
        except Exception as e:
            raise Exception(222, e.args)


class ManageCore (ManageCoreBase):

    def __init__(self, neighborhood, street, number, city, user):
        """
        Construtor
        :param neighborhood: bairro da importação
        :param street: rua da importação
        :param number: número da importação
        :param city: cidade da importação
        """
        super().__init__(neighborhood, city, user)
        self.street = street
        self.number = number

        self.set_info_address()  # Configura o endereço completo que será usado na busca

    def is_address_valid(self):
        """
        Se os dados de endereço enviados para a classe não possuírem bairro e rua, o geocode não funcionará
        :return: True se tiver bairro ou rua. False se não tiver os dois.
        """
        if self.neighborhood_name == "" and self.street == "":
            print("O endereço não possui bairro (%s) ou rua (%s)." % (self.neighborhood_name, self.street))
            return False
        return True

    def set_info_address(self):
        """
        Formata o endereço que será usado para geocode.

        1. Zera o formatted_address (nesse momento ele sempre está zerado, mas no futuro quando o framework estiver
        mais bem implementado isso será importante)
        2. Analisa se os dados enviados são válidos
        :return: None. Apenas seta o info_address
        """
        try:
            city_location = ' - ' + self.city + ", " + self.state

            if self.is_address_valid():
                if self.street:
                    self.formatted_address += self.street + " "
                if self.number and self.number != 'S/N':
                    self.formatted_address += self.number + ", "
                if self.get_neighborhood_data_name():
                    self.formatted_address += self.get_neighborhood_data_name()
                self.formatted_address += city_location
            else:
                raise NeighborhoodOrStreetNotSetup("Bairro: %s" % self.neighborhood_name, "Rua: %s" % self.street)
        except NeighborhoodOrStreetNotSetup as n:
            self.report.add_error(cod=311, args=n.args)
            raise n
        except Exception as e:
            self.report.add_error(cod=312, args=e.args)
            raise e

    def get_bounds(self):
        """
        tenta buscar os bounds do bairro, se não der certo envia os bounds da cidade.

        1. Inicia a var que será retornada (bounds) com os bounds da cidade.
        2. Se houver dados no bairro iniciado com o set_info_address, pega os bounds do bairro e atribui a var bounds.
        Se não, busca o bairro com o get_neighborhood do managerneighborhood, buscando num geocode.
        Caso nenhuma destas opções seja utilizada, é usado os bounds da cidade.
        :return: bounds
        """
        bounds = self.get_city_bounds()

        try:
            if self.get_neighborhood_bounds():
                bounds = self.get_neighborhood_bounds()
        except Exception as e:
            self.report.add_error(cod=321, args=("Erro de análise de geometria do bairro. Verifique se o bairro "
                                                 "informado está no sistema que avalia a análise de confiança. "
                                                 "Este erro pode ter acontecido por dificuldades de analisar os dados "
                                                 "geométricos do bairro e da cidade.", e.args))
        finally:
            return bounds

    def get_geocode(self, auto_bound=None):
        """
        Este método é o responsável por retornar a latitude e a longitude do endereço formulado no set_info_address()
        :param auto_bound: Se for passado por parâmetro, o geocode é utilizado com ele e não de forma dinâmica
        :return: dicionário retornado pela biblioteca da api google maps
        """
        try:
            if auto_bound:
                bounds = auto_bound
            else:
                bounds = self.get_bounds()

            print('PESQUISANDO NO GEOCODE::', self.formatted_address)
            self.report.add_result_search_address(self.formatted_address)

            geocode = self.gmaps.geocode(address=self.formatted_address,
                                         language='pt-BR',
                                         bounds=bounds)[0]
            if geocode:
                return geocode
            else:
                raise GeocodeNotFound('Nenhum endereço encontrado para: %s' % self.formatted_address)
        except GeocodeNotFound as g:
            print(g.__repr__())
            self.report.add_error(cod=331, args=g.args)
            raise g
        except Exception as e:
            print("Erro desconhecido no get_geocode", e.__repr__())
            self.report.add_error(cod=332, args=e.args)
            raise e

    def geocode_is_valid(self, lat_lng_geocode):
        """
        :param lat_lng_geocode: {lat: ..., lng: ...}
        :return: true se estiver ok, false se não
        Verifica se está dentro da cidade e do bairro
        """
        try:
            if self.get_distance_to_city_center(lat_lng_geocode) <= self.get_city_max_distance():
                self.report.add_result_confidence(21)
                # está dentro da cidade. Está dentro do bairro?
                if self.is_in_neighborhood_bounds(location=lat_lng_geocode):
                    self.report.add_result_confidence(23)
                    return True
                else:
                    # Não está dentro do bairro. Está muito longe?
                    distance_neighborhood = self.distance_neighbor(lat_lng=lat_lng_geocode, metric='meters')
                    max_distance = self.get_neighborhood_max_distance()
                    if distance_neighborhood > max_distance:
                        # longe
                        self.report.add_result_confidence(15, warning="dist_max: %s m, dist: %s m" %
                                                                      (distance_neighborhood, max_distance))
                        return False
                    else:
                        # perto
                        self.report.add_result_confidence(22)
                        return True
            else:
                # está fora da cidade
                self.report.add_result_confidence(14)
                return False
        except MaxDistanceNeighborhoodNotFound as m:
            print(m.__repr__())
            self.report.add_error(cod=341)
            self.report.add_result_confidence(0)
            return False
        except AssertionError as a:
            print(a.__repr__())
            self.report.add_error(cod=342, args=a.args)
            return False
        except Exception as e:
            print(e.__repr__())
            self.report.add_error(cod=343, args=e.args)
            return False

    def get_location(self):
        """
        Método que inicia o processo de aquisição dos dados de lat e lng.
        1. Seta as informações de endereço
        :return: dic {'lat':..., 'lng':...}
        """
        try:

            geocode = self.get_geocode()

            lat_lng = self.get_lat_lng(geocode)
            self.report.add_result_geocode(lat=lat_lng['lat'], lng=lat_lng['lng'])

            if self.geocode_is_valid(lat_lng):
                pass
            else:
                raise GeocodeNotTrusted("Não foi possível encontrar uma localização "
                                        "satisfatória para %s" % self.formatted_address)
        except NeighborhoodOrStreetNotSetup as n:
            print(n.__repr__())
        except GeocodeNotTrusted as g:
            self.report.add_result_confidence(12)
            self.report.add_error(351, args=g.args)
        except GeocodeNotFound as g:
            print(g.__repr__(), "criando ou recuperando blacklist")
            blacklist = ManageBlackList().create_or_retrieve_blacklist(
                city=self.city,
                neighborhood=self.neighborhood_name,
                rua=self.street,
                endereco_completo=self.formatted_address,
                usuario=self.user)
            self.report.add_blacklist(blacklist)
            self.report.add_result_confidence(16)
        except CreateBlackListError as c:
            print(354, c.__repr__())
            self.report.add_error(354, args=c.args)
            self.report.add_result_confidence(10)
        except Exception as e:
            self.report.add_result_confidence(10)
            self.report.add_error(cod=353, args=e.args)
        finally:
            return self.report.get_report()
