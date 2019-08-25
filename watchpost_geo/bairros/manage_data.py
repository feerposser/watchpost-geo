from django.core.exceptions import ObjectDoesNotExist
from difflib import SequenceMatcher
from geopy import distance
import googlemaps

from .models import ModelBairro, ModelBairroAuxiliar
from cidades.models import ModelCidade
from cidades.manage_data import ManageCity
from core.report import Report
from alg_utils.watchpost_exceptions import MaxDistanceNeighborhoodNotFound, NeighborhoodGeocodeNotFound, \
    NotRighNeighborhood, CreateNeighborhoodError, NeighborhoodOutsideCity, NeighborhoodNotInDB

gmaps = googlemaps.Client(key='AIzaSyBYoU0ZrNNsAK-56cJBMK2LooCa5RtgqfQ')


class Neighborhood:

    def __init__(self, neighborhood_name, city):
        self.neighborhood_name = neighborhood_name
        self.city = city
        self.report = Report()

    def get_report(self):
        return self.report.report

    @staticmethod
    def neighborhood_exists_in_city(city, neighborhood, status="A"):
        """
        Analisa se um bairro existe em uma determinada cidade. Faz a busca em modelbairro e modelbairroauxiliar
        :param city: objecto ModelCidade ou id int
        :param neighborhood: Nome do bairro
        :param status: status do objeto de busca. A = Ativo (default), I = Indefinido
        :return: se existir retorna true, senão false
        """
        result, where_from = None, None

        print('city:', city, '\nneigh:', repr(neighborhood), neighborhood, type(neighborhood), '\n')

        try:
            assert status == 'A' or status == 'D' or status == 'I', "parâmetro status inválido"
            assert isinstance(neighborhood, str) and str(neighborhood).replace(" ", "") != "", \
                "parâmetro neighborhood inválido"

            if isinstance(city, str):
                city = ManageCity.get_city_model(city)
            elif isinstance(city, ManageCity):
                city = city.get_city_data()

            if ModelBairro.objects.filter(nome__contains=neighborhood, cidade=city, status=status).exists():
                result = ModelBairro.objects.filter(nome__contains=neighborhood, cidade=city, status=status)[0]
                where_from = ModelBairro
            elif ModelBairroAuxiliar.objects.filter(nome__contains=neighborhood, cidade=city, status=status).exists():
                result = ModelBairroAuxiliar.objects.filter(nome__contains=neighborhood, cidade=city)[0]
                result = result.fk_bairro
                where_from = ModelBairroAuxiliar
            else:
                raise ObjectDoesNotExist("Bairro '%s' - cidade '%s' não encontrados." % (neighborhood, city))
        except ObjectDoesNotExist as o:
            print(511, o.__repr__())
            result, where_from = None, None
        except AssertionError as a:
            print(512, a.__repr__())
            result, where_from = None, None
        except IndexError as i:
            print(513, i.__repr__(), 'Erro provocado porque o .filter não encontrou nenhum bairro com os parâmetros '
                                     'especificados')
            result, where_from = None, None
        except ValueError as v:
            print(514, v.__repr__(), 'O erro provavelmente foi causado porque city não é um ModelCidade')
            result, where_from = None, None
        except Exception as e:
            print(515, e.__repr__(), 'erro desconhecido')
            result, where_from = None, None
        finally:
            print(':', result, where_from)
            return result, where_from

    def get_neighborhood(self, id=False, as_dict=False):
        """
        :param as_dict: Se for True retorna como dicionário
        :param id: se for passado por parâmetro então deve ser dada preferência para o id
        :return: Se encontrar algo no banco retorna o objeto, senão None
        Busca o bairro no banco de dados
        """
        try:
            if id:
                neighborhood = ModelBairro.objects.get(id=id, status='A')
            else:
                assert str(self.neighborhood_name).replace(" ", "") != "", "parâmetro neighborhood_name inválido"
                neighborhood = ModelBairro.objects.filter(nome__contains=self.neighborhood_name, status='A')[0]
            if neighborhood:
                if as_dict:
                    neighborhood = neighborhood.__dict__
                return neighborhood

            raise NeighborhoodNotInDB("Bairro não encontrado no get_neighborhood.")
        except NeighborhoodNotInDB as n:
            print(521, n.__repr__())
            self.report.add_error(cod=521)
            return None
        except Exception as e:
            print(522, e.__repr__())
            self.report.add_error(cod=522, args=e.args)
            return None

    def get_neighborhood_in_city(self, as_dict=False, status='A'):
        try:
            assert status == 'A' or status == 'D' or status == 'I', "parâmetro status inválido"
            assert str(self.neighborhood_name).replace(" ", "") != "", "parâmetro neighborhood_name inválido"

            city = ManageCity.get_city_model(self.city)

            if ModelBairro.objects.filter(
                    nome__contains=self.neighborhood_name, cidade=city, status=status).exists():
                neighborhood = ModelBairro.objects.get(nome__contains=self.neighborhood_name, cidade=city,
                                                       status=status)
            elif ModelBairroAuxiliar.objects.filter(nome__contains=self.neighborhood_name, cidade=city).exists():
                neighborhood = ModelBairroAuxiliar.objects.get(nome__contains=self.neighborhood_name, cidade=city)
                neighborhood = neighborhood.fk_bairro
            else:
                neighborhood = False

            if neighborhood:
                if as_dict:
                    neighborhood = neighborhood.__dict__
                return neighborhood
            raise Exception('Bairro não encontrado.')
        except AssertionError as a:
            print(531, a.__repr__())
        except Exception as e:
            print(532, e.__repr__())
            return None

    @staticmethod
    def best_sequence_matcher(queryset, neighborhood, value=0.3):
        """
        Este método serve para retornar apenas um único dado do queryset com mais compatibilidade com o bairro
        desejado.
        :param queryset: Iterável QuerySet com objetos ModelBairro
        :param neighborhood: Nome do bairro. str
        :param value: double(0.- a 1.0) que será usado para comparar com o retorno do SequeneMatcher
        :return:
        """
        lvl_match = -1
        match = None

        for n in queryset:
            print(n.nome, '.-.', neighborhood, '.')
            lvl = SequenceMatcher(None, neighborhood, n.nome).ratio()
            if lvl > lvl_match:
                lvl_match = lvl
                match = n
        print('BAIRRO: level match:', lvl_match, match)
        if lvl_match < value:
            return None

        return match

    @staticmethod
    def dictlatlng_to_tuplelatlng(lat_lng):
        if isinstance(lat_lng, dict):
            if 'lat' and 'lng' in lat_lng:
                return lat_lng['lat'], lat_lng['lng']

    @staticmethod
    def get_wrong_neighborhood_info(name):
        """
        OK
        Utilizado para recuperar informações dos bairros comumente inseridos com nomes errados.
        :param name: nome do bairro
        :return: objeto com nome e fk dos dados corretos ou none
        """
        try:
            assert str(name).replace(" ", "") != "", "parâmetro name inválido"
            return ModelBairroAuxiliar.objects.get(nome=name)
        except AssertionError as a:
            print(541, a.__repr__())
            return None
        except Exception as e:
            print(542, e.__repr__())
            return None

    def get_aux_neighborhood_in_city(self, as_dict=True):
        """
        Retorna o bairro correto através do nome errado (busca na base de bairros auxiliar com nomes incorretos).
        :return:
        """
        try:
            city = ManageCity.get_city_model(self.city)
            neighborhood_aux = ModelBairroAuxiliar.objects.filter(nome__icontains=self.neighborhood_name,
                                                                  cidade=city)[0]
            if neighborhood_aux:
                if as_dict:
                    return neighborhood_aux.fk_bairro.__dict__
                return neighborhood_aux.fk_bairro
        except Exception as e:
            print(551, e.__repr__())
            return None


class HandleNeighborhood(Neighborhood):

    google_maps_neighborhood_types = ('sublocality', 'sublocality_level_1')

    def __init__(self, neighborhood, city):
        super().__init__(neighborhood, city)

    @staticmethod
    def address_exists(neighborhood, city, status='ALL'):
        """
        Verifica se um endereço encontrado pelo geocode já está registrado no banco de dados.
        A diferença deste método para o get_neighborhood é que este analisa o campo endereço para ver se já está
        georreferenciado. No get_neigh.. normal é utilizado apenas o nome completo do bairro.
        :param neighborhood: estrutura geocode
        :param city: objeto ModelCidade que será usado para realizar busca no banco de dados
        :param get_all_status: bool - True se o método deve encontrar resultados independente do status do bairro,
        false se deve procurar por status específicos usando o parâmetro status.
        :param status: status do dado no banco, se está ativo ou desativo (ModelBairro)
        :return: Objeto encontrado se existir, false se não existir
        """

        formatted_address = neighborhood['formatted_address']
        result = False

        try:
            assert str(formatted_address).replace(" ", "") != "", \
                "parâmetro formatted_address inválido: '%s'" % formatted_address
            assert isinstance(city, ModelCidade), \
                "parâmetro city deve ser instância de ModelCidade ao invés de '%s'" % str(type(city))
            assert status == 'A' or status == 'D' or status == 'I' or status == 'ALL', \
                "parâmetro status inválido '%s'. status deve ser igual a A, D, I ou ALL"

            query = ModelBairro.objects.filter(endereco=formatted_address, cidade=city)

            if query:
                if status != 'ALL':
                    query = query.filter(status=status)[0]

                result = query[0]
            else:
                raise ObjectDoesNotExist("endereço não encontrado")
        except ObjectDoesNotExist as o:
            print(611, o.__repr__())
        except AssertionError as a:
            print(612, a.__repr__())
        except Exception as e:
            print(613, e.__repr__())
        finally:
            return result

    def geocode_neighborhood(self, city_bounds):
        """
        Este método retorna o geocode de um bairro
        :param city_bounds: dict - Bounds da cidade
        :return: estrutura geocode completa ou none
        """
        try:
            city_bounds = city_bounds

            if self.neighborhood_name:
                search_address = self.neighborhood_name
            else:
                raise AssertionError("Bairro inexistente")

            search_address += ', ' + self.city + ', RS - Brasil'
            print(search_address)
            geocode = gmaps.geocode(address=search_address, language='pt-BR', bounds=city_bounds)[0]

            if geocode:
                return geocode
            else:
                return None
        except AssertionError as a:
            print(621, a.__repr__())
            return None
        except Exception as e:
            print(622, e.__repr__())
            return None

    def search_geocode_neighborhood(self):
        """
        Este método implementa várias funcionalidades de outros métodos. Deve ser chamado quando um bairro não foi
        encontrado no banco de dados. Isso significa que o bairro não foi cadastrado. Este método fará:
        1. Buscará o geocode com os bounds da cidade
        :param city_bounds:
        :param as_dict:
        :return:
        """
        manage_city = ManageCity(self.city)

        try:

            neighborhood_geocode = self.geocode_neighborhood(city_bounds=manage_city.get_city_bounds())

            if neighborhood_geocode:
                if self.is_neighborhood(neighborhood_geocode['types']):
                    neighborhood_exist = self.address_exists(neighborhood_geocode,
                                                             city=manage_city.get_city_data())
                    if neighborhood_exist:
                        print("O bairro já existia no banco de dados")
                        if self.is_right_neighborhood(neighborhood=neighborhood_exist, geocode=False, value=0.2):
                            self.create_neighborhood_aux(name=self.neighborhood_name,
                                                         neighborhood=neighborhood_exist,
                                                         city=manage_city.get_city_data())
                            return neighborhood_exist
                        else:
                            raise NotRighNeighborhood("Não encontrou o bairro correto. '%s' : '%s'" %
                                                      (self.neighborhood_name, self.get_neighborhood_name_geocode(
                                                          neighborhood_geocode)))
                    else:
                        print("O bairro não existia no banco de dados")
                        print("Verificar se o bairro está dentro da cidade")
                        if manage_city.is_inside_city(neighborhood_geocode):
                            print('Está dentro da cidade')
                            if self.is_right_neighborhood(neighborhood_geocode):
                                print('É o bairro certo')
                                print("criando o bairro no banco de dados")
                                new_neighborhood = self.create_neighborhood(self.get_geocode_neighborhood_info(
                                    neighborhood_geocode), manage_city.get_city_data())
                                print("Se o nome do bairro enviado for diferente do geocode, criar um aux também")
                                if self.neighborhood_name != self.get_neighborhood_name_geocode(neighborhood_geocode):
                                    self.create_neighborhood_aux(
                                        name=self.neighborhood_name,
                                        city=manage_city.get_city_data(),
                                        neighborhood=new_neighborhood)

                                return True
                            else:
                                print("Não é o bairro correto")
                                raise NotRighNeighborhood("Bairro encontrado '%s' diferente do informado '%s'" %
                                                          (neighborhood_geocode['address'], self.neighborhood_name))
                        else:
                            print("Fora da cidade")
                            raise NeighborhoodOutsideCity("O bairro encontrado não pertence a cidade informada.")
                else:
                    print('não é bairro')
                    raise NeighborhoodGeocodeNotFound("Bairro não encontrado no banco de dados e no geocode")
            else:
                raise NeighborhoodGeocodeNotFound("Geocode de '%s' não encontrado" % self.neighborhood_name)
        except IndexError as e:
            print(631, e.__repr__())
            raise CreateNeighborhoodError(631, "Nenhum bairro encontrado para '%s'. Descrição: -%s" %
                                          (self.neighborhood_name, e))
        except NeighborhoodOutsideCity as n:
            print(632, n.__repr__())
            raise CreateNeighborhoodError(632, n.__repr__())
        except NotRighNeighborhood as r:
            print(633, r.__repr__())
            raise CreateNeighborhoodError(633, r.__repr__)
        except CreateNeighborhoodError as c:
            print(634, c.__repr__())
            raise CreateNeighborhoodError(634, c.args)
        except NeighborhoodGeocodeNotFound as n:
            print(635, n.__repr__())
            raise CreateNeighborhoodError(635, n.__repr__())
        except AssertionError as a:
            print(636, a.__repr__())
            raise CreateNeighborhoodError(636, "Erro de validação", a.__repr__())
        except Exception as e:
            print(637, e.__repr__())
            raise CreateNeighborhoodError(637, "Erro desconhecido ao criar o bairro: '%s'" % e.__repr__())

    def is_right_neighborhood(self, neighborhood, geocode=True, value=0.3):
        """
        Analisa a compatibilidade de duas strings. Uma é um dado encontrado pelo sistema, outra um dado imputado
        pelo usuário. Se as strings coincidirem, significa que o dado encontrado pelo sistema é referente ao
        dado que o usuário está buscando.
        :param neighborhood: Dado do sistema a ser comparado com o dado imputado.
        :param geocode: se for true então o método está recebendo uma estrutura geocode completa da API e deve analisar
        as strings levando isso em consideração. Se for false então é um objeto ModelBairro.
        :param value: valor usado no sequencematcher
        :return: true se coindidir, se não False
        """

        try:
            if geocode:
                for item in neighborhood['address_components']:
                    if 'sublocality_level_1' in item['types']:
                        if SequenceMatcher(None,
                                           str(item['long_name']).upper(),
                                           str(self.neighborhood_name).upper()).ratio() > value:
                            return True
            else:
                if SequenceMatcher(None, neighborhood.nome, str(self.neighborhood_name).upper()).ratio() > value:
                    return True

            return False
        except Exception as e:
            print(641, e.__repr__())
            return False

    def get_neighborhood_name_geocode(self, geocode):
        """
        Função utilizada para encontrar o nome completo de um bairro a partir da estrutura geocode completa.
        :param geocode: estrutura geocode completa
        :return: nome do bairro, mas se não encontrou um bairro na estrutura address components, retorna none
        """
        try:
            assert isinstance(geocode, dict), "parâmetro 'geocode' inválido. Ele deve ser um dict"

            name = None

            for address_components in geocode['address_components']:
                if self.is_neighborhood(address_components['types']):
                    name = address_components['long_name']
            return name

        except AssertionError as a:
            print(651, a.__repr__())
            raise AssertionError(651, a.args)
        except Exception as e:
            print(652, e.__repr__())
            raise Exception(652, e.args)

    def get_geocode_neighborhood_info(self, geocode, neighborhood_name=""):
        """
        Dado uma determinada estrutura de googlema maps geocode api, retorna um dict com o formato dos atributos aceitos
        pelo model do banco de dados.
        :param geocode: strutura geocode api
        :param neighborhood_name:
        :return: dict com o formato aceito pelo model do banco de dados.
        """
        try:
            name = ""
            if neighborhood_name:
                name = neighborhood_name
            else:
                name = self.get_neighborhood_name_geocode(geocode)

            return {
                'name': name,
                'city': self.city,
                'bounds_northeast_lat': geocode['geometry']['bounds']['northeast']['lat'],
                'bounds_northeast_lng': geocode['geometry']['bounds']['northeast']['lng'],
                'bounds_southwest_lat': geocode['geometry']['bounds']['southwest']['lat'],
                'bounds_southwest_lng': geocode['geometry']['bounds']['southwest']['lng'],
                'latitude': geocode['geometry']['location']['lat'],
                'longitude': geocode['geometry']['location']['lng'],
                'address': geocode['formatted_address']
            }
        except AssertionError as a:
            print(661, a.__repr__())
            raise AssertionError(661, a.args)
        except Exception as e:
            print(662, e.__repr__())
            raise Exception(662, e.args)

    def is_neighborhood(self, list_types):
        """
        Serve para saber se um dado encontrado é um bairro ou não segundo o GMAPS API
        :param list_types: list com os tipos encontrados pela API do googlemaps.
        :return: True se for um bairro, false se não for
        """
        result = False

        for item in list_types:
            if item in self.google_maps_neighborhood_types:
                result = True
        return result

    @staticmethod
    def create_neighborhood(neighborhood, city, status=None):
        """
        Cria um novo registro de bairro
        :param neighborhood: dicionário com as informações e keys de um modelo ModelBairro
        :param city: obj ModelCidade
        :param status: status do objeto
        :return: objeto criato ou exception
        """
        try:
            assert isinstance(city, ModelCidade), "parâmetro city deve ser um objeto ModelCidade"
            if status:
                assert status == 'A' or status == 'I' or status == 'D', "parâmetro status deve ser 'A', 'I' ou 'D'"

            mb = ModelBairro()
            mb.nome = str(neighborhood['name']).upper()  # todo: está indo como none
            mb.cidade = city

            if 'bounds_northeast_lat' in neighborhood:
                mb.bounds_northeast_lat = neighborhood['bounds_northeast_lat']
            if 'bounds_northeast_lng' in neighborhood:
                mb.bounds_northeast_lng = neighborhood['bounds_northeast_lng']
            if 'bounds_southwest_lat' in neighborhood:
                mb.bounds_southwest_lat = neighborhood['bounds_southwest_lat']
            if 'bounds_southwest_lng' in neighborhood:
                mb.bounds_southwest_lng = neighborhood['bounds_southwest_lng']
            if 'latitude' in neighborhood:
                mb.latitude = neighborhood['latitude']
            if 'longitude' in neighborhood:
                mb.longitude = neighborhood['longitude']
            if 'address' in neighborhood:
                mb.endereco = neighborhood['address']
            if status:
                mb.status = status
            mb.save()

            return mb

        except AssertionError as a:
            print(671, a.__repr__())
            raise CreateNeighborhoodError(671, "Erro na criação do bairro '%s'" % a.__repr__())
        except Exception as e:
            print(672, e.__repr__())
            raise CreateNeighborhoodError(672, "Erro desconhecido na criação do bairro '%s'" % e.__repr__())

    @staticmethod
    def create_neighborhood_aux(name, city, neighborhood):
        """
        cria um novo registro no modelo de bairros auxiliares
        :param wrong_name: str - nome incorreto inserido pelo usuário
        :param neighborhood: Obj ModelBairro - objeto que será apontado
        :return: Objeto criato, caso de erro Exception
        """
        try:
            assert isinstance(city, ModelCidade), "parâmetro 'city' deve ser um obj 'ModelCidade'"
            if not ModelBairroAuxiliar.objects.filter(nome=name).exists():
                return ModelBairroAuxiliar.objects.create(
                    nome=name,
                    cidade=city,
                    fk_bairro=neighborhood
                )
        except AssertionError as a:
            print(682, a.__repr__())
            raise AssertionError(682, a.args)
        except Exception as e:
            print(681, e.__repr__())
            raise Exception(681, "Erro ao inserir bairro auxiliar: %s" % repr(e))


class ManageNeighborhood(HandleNeighborhood):
    """
    Classe utilizada apenas caso o bairro exista no banco de dados.
    """

    def __init__(self, neighborhoood, city):
        """
        Tenta buscar o bairro no banco de dados de bairro e bairro auxiliar.
        :param neighborhoood:
        :param city:
        """
        super().__init__(neighborhoood, city)

        try:
            assert neighborhoood != "", "parametro 'name' não deve estar vazio"

            neighborhood_data = self.get_neighborhood_in_city(as_dict=True)

            if neighborhood_data:
                self.neighborhood_data = neighborhood_data
            else:
                neighborhood_data = self.get_aux_neighborhood_in_city()
                if not neighborhood_data:
                    raise NeighborhoodNotInDB("Bairro '%s' não encontrado no banco de dados." % self.neighborhood_name)
                self.neighborhood_data = neighborhood_data
        except AssertionError as a:
            print(711, a.__repr__(), a.args)
        except NeighborhoodNotInDB as n:
            print(712, n.__repr__(), n.args)
        except Exception as e:
            print(713, e.__repr__(), e.args)

    def get_neighborhood_bounds(self, as_dict=True):
        """
        Retorna os valores dos bounds
        :return:
        """
        try:
            if as_dict:
                return {
                    'northeast': {
                        'lat': self.neighborhood_data['bounds_northeast_lat'],
                        'lng': self.neighborhood_data['bounds_northeast_lng']
                    },
                    'southwest': {
                        'lat': self.neighborhood_data['bounds_southwest_lat'],
                        'lng': self.neighborhood_data['bounds_southwest_lng']
                    }
                }
        except Exception as e:
            print(721, e.__repr__())
            return None

    def get_neighborhood_center(self, as_tuple=True):
        try:
            if not as_tuple:
                return {
                    'center': {
                        'lat': self.neighborhood_data['latitude'],
                        'lng': self.neighborhood_data['longitude']
                    }
                }
            else:
                return self.neighborhood_data['latitude'], self.neighborhood_data['longitude']
        except Exception as e:
            print(731, e.__repr__())
            raise Exception(731, e.args)

    def distance_neighbor(self, lat_lng, metric='km'):
        """
        Retorna a distância do centro do bairro do incidente em metros ou kilometros
        :param lat_lng: latitude e longitude do incidente
        :param metric: km = kilometros, meters = metros
        :return:
        """
        try:
            assert metric == 'km' or metric == 'meters', "parâmetro 'metric' inválido deve ser 'km' ou 'meters' e não" \
                                                         " %s" % metric
            assert isinstance(metric, str), "parâmetro 'metric' deve ser string e não %s" % type(metric)

            neighborhood_center = self.get_neighborhood_center()
            lat_lng = self.dictlatlng_to_tuplelatlng(lat_lng)

            if neighborhood_center:
                if metric == 'km':
                    return distance.distance(lat_lng, neighborhood_center).km
                elif metric == 'meters':
                    return distance.distance(lat_lng,  neighborhood_center).meters
            else:
                raise Exception('Erro desconhecido. ManageNeighborhood.distance_neighbor. sem neighborhood_center para'
                                ' %s' % self.neighborhood_data)
        except AssertionError as a:
            print(741, a.__repr__())
            raise AssertionError(741, a.args)
        except Exception as e:
            print(742, e.__repr__())
            raise Exception(742, e.args)

    def is_in_neighborhood_bounds(self, location):
        """
        Verifica se uma posição geográfica está dentro da área de um bairro
        :param location: lat e lng (dict)
        :return: true se estiver, false se não
        northeast: NE -> nordeste - direita em cima
        southweast: SW -> sudoeste - esquerda em baixo
        Na posição meridional de PF as regras para que um ponto geográfico esteja fora da área do bairro são:
        A latitude do ponto ser menor que a latitude sudoeste e maior que a latitude nordeste
        A longitude do ponto ser menor que a longitude sudoeste ou maior que a longitude nordeste
        """
        neighborhood_bounds = self.get_neighborhood_bounds()

        try:
            if location['lat'] > neighborhood_bounds['northeast']['lat'] or \
                    location['lat'] < neighborhood_bounds['southwest']['lat'] or \
                    location['lng'] > neighborhood_bounds['northeast']['lng'] or \
                    location['lng'] < neighborhood_bounds['southwest']['lng']:
                return False
            return True
        except Exception as e:
            print(751, e.__repr__())
            raise Exception(751, 'Erro no ManageNeighborhood.is_in_neighborhood_bounds', e.args)

    def get_neighborhood_max_distance(self):
        try:
            if self.neighborhood_data and 'distancia_maxima' in self.neighborhood_data:
                return self.neighborhood_data['distancia_maxima']
            else:
                raise MaxDistanceNeighborhoodNotFound("distancia máxima do bairro não encontrada.")
        except MaxDistanceNeighborhoodNotFound as m:
            print(761, m.__repr__())
            raise MaxDistanceNeighborhoodNotFound(761, m.args)
        except Exception as e:
            print(762, e.__repr__())
            raise Exception(762, e.args)

    def get_neighborhood_data_name(self, as_dict=True):
        try:
            if as_dict:
                if isinstance(self.neighborhood_data, dict) and 'nome' in self.neighborhood_data:
                    return self.neighborhood_data['nome']
            else:
                return self.neighborhood_data.nome
            return self.neighborhood_name
        except Exception as e:
            print(771, e.__repr__())
            return ""

