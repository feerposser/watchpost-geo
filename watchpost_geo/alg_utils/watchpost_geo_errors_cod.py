from django.core.exceptions import ObjectDoesNotExist

from .watchpost_exceptions import *


class ErrorsCode:

    def __init__(self):
        self.__error_not_identify = {"description": "Erro não mapeado", "error": Exception}
        self.__obj_dn_exists = {"description": "A busca pelo modelo não retornou nenhum objeto",
                                "error": ObjectDoesNotExist}
        self.__errors_code = {
            111: {"description": None, "error": None},
            112: {"description": None, "error": None},
            113: {
                "description": "Parâmetro 'city' vazio",
                "error": ParamCityEmpty},
            114: {
                "description": "Parâmetro 'neighborhood' vazio",
                "error": ParamNeighborhoodEmpty},
            115: self.__error_not_identify,
            121: {
                "description": "Bairro desconhecido nos sistemas.",
                "error": CreateNeighborhoodError},
            122: {
                "description": "A cidade não está cadastrada no banco de dados",
                "error": CityNotInDB},
            123: {
                "description": "O geocode encontrado não é confiável pois não passou pelo teste de validação",
                "error": GeocodeNotTrusted},
            124: {
                "description": "Dadosgeográficos do bairro não encontrados",
                "error": NeighborhoodGeocodeNotFound},
            125: self.__error_not_identify,
            211: self.__error_not_identify,
            221: {
                "description": "Erro de validação causado porque algum dos elementos necessários para geração dos "
                               "bounds em formato de dicionário vindos do parâmetro 'neighborhood_model_obj' não está "
                               "presente.",
                "error": AssertionError},
            222: self.__error_not_identify,
            311: {
                "description": "Bairro ou rua não definidos ou vazios",
                "error": NeighborhoodOrStreetNotSetup},
            312: self.__error_not_identify,
            321: self.__error_not_identify,
            331: {
                "description": "Nenhum dado foi retornado pela API",
                "error": GeocodeNotFound},
            332: self.__error_not_identify,
            341: {
                "description": "Distância máxima do bairro não encontrada",
                "error": MaxDistanceNeighborhoodNotFound},
            342: {
                "description": "Erro de validação vinda de outro método",
                "error": AssertionError},
            343: self.__error_not_identify,
            351: {
                "description": "O endereço possui um baixo nível de confiança de acordo com os parâmetros do sistema.",
                "error": GeocodeNotTrusted},
            352: {
                "description": "Erro retornado pelo get_geocode.",
                "error": GeocodeNotFound},
            353: self.__error_not_identify,
            354: {
                "description": "Erro ao criar uma blacklist",
                "error": CreateBlackListError},
            411: {
                "description": "Erro causado porque o parâmetro metric deve ser igual a 'km' ou 'meters'",
                "error": AssertionError},
            412: self.__error_not_identify,
            421: {
                "description": "Erro causado porque o tipo do parâmetro location deve ser dict ou tuple. "
                               "Ainda pode ter sido causado porque a versão atual do sistema não possibilita a "
                               "manipulação de location como dict",
                "error": AssertionError},
            422: self.__error_not_identify,
            431: self.__obj_dn_exists,
            432: self.__error_not_identify,
            511: self.__obj_dn_exists,
            512: {
                "description": "Erro de validação. Pode ser provocado porque o parâmetro status deve ser igual a "
                               "'A' ou 'D' ou 'I' / parâmetro neighborhood deve ser str e não pode estar vazia",
                "error": AssertionError},
            513: {
                "description": "Erro provocado porque o .filter do ModelBairro não retornou nenhum bairro na lista",
                "error": IndexError},
            514: {
                "description": "Possivelmente provocado porque o parâmetro city não é um objeto ModelCidade",
                "error": ValueError},
            515: self.__error_not_identify,
            521: {
                "description": "A busca pelo modelo não retornou nenhum objeto",
                "error": NeighborhoodNotInDB},
            522: self.__error_not_identify,
            531: {
                "description": "Erro de validação. Parâmetro status deve ser igual a 'A', 'D' ou 'I' / "
                               "Parâmetro da classe neighborhood_name inválido.",
                "error": AssertionError},
            532: self.__error_not_identify,
            541: {
                "description": "Erro de validação. Parâmetro name vazio.",
                "error": AssertionError},
            542: self.__error_not_identify,
            551: self.__error_not_identify,
            611: self.__obj_dn_exists,
            612: {
                "description": "Erro de validação. Parâmetro 'formatted_address' vazio. Parâmetro 'city' não é um obj "
                               "ModelCidade. Parâmetro 'status' é diferente de 'A' ou 'D' ou 'I' ou 'ALL'",
                "error": AssertionError},
            613: self.__error_not_identify,
            621: {
                "description": "Erro de validação. Parâmetro 'neighbrhood_name' da classe vazio.",
                "error": AssertionError},
            622: self.__error_not_identify,
            631: {
                "description": "Nenhum bairro encontrado no banco de dados",
                "error": IndexError},
            632: {
                "description": "O bairro encontrado está fora da cidade",
                "error": NeighborhoodOutsideCity},
            633: {
                "description": "O nome do bairro encontrado é muito diferente do nome informado pelo usuário",
                "error": NotRighNeighborhood},
            634: {
                "description": "Erro ao criar o bairro no banco de dados",
                "error": CreateNeighborhoodError},
            635: {
                "description": "Não foi possível encontrar o banco de dados na busca do geocode",
                "error": NeighborhoodGeocodeNotFound},
            636: {
                "description": "Erro de validação. Pode ser provocado por muitas situações. Analisar o traceback "
                               "retornado pela classe",
                "error": AssertionError},
            637: self.__error_not_identify,
            641: self.__error_not_identify,
            651: {
                "description": "Erro de validação. Possivelmente o parâmetro geocode não está no formato dict",
                "error": AssertionError},
            652: self.__error_not_identify,
            661: {
                "description": "Erro de validação. Analisar traceback da classe",
                "error": AssertionError},
            662: self.__error_not_identify,
            671: {
                "description": "Erro de validação: Parâmetro city não é um ModelCidade ou status é diferente de 'A', "
                               "'D' ou 'I'",
                "error": AssertionError},
            672: self.__error_not_identify,
            681: self.__error_not_identify,
            711: {
                "description": "Erro de validação. Parâmetro 'neighborhood' vazio",
                "error": AssertionError},
            712: {
                "description": "Bairro não encontrado no banco de dados para a cidade solicitada",
                "error": NeighborhoodNotInDB},
            713: self.__error_not_identify,
            721: self.__error_not_identify,
            731: self.__error_not_identify,
            741: {
                "description": "Erro de validação. 'metric' deve ser igual ' km' ou 'meters'. 'metric' deve ser str.",
                "error": AssertionError},
            742: self.__error_not_identify,
            751: self.__error_not_identify,
            761: {
                "description": "Distância máxima do bairro não encontrada em neighborhood_data['distancia_maxima']",
                "error": MaxDistanceNeighborhoodNotFound},
            762: self.__error_not_identify,
            771: self.__error_not_identify,
            811: {
                "description": "Erro de validação. city não é um objeto ModelCidade",
                "error": AssertionError},
            812: self.__error_not_identify,
            821: self.__obj_dn_exists,
            822: self.__error_not_identify
        }

    def get_error(self, cod):

        none_error = {"description": None, "error": None}

        try:
            assert isinstance(cod, int), "parâmetro 'cod' deve ser 'int' e não '%s'" % str(type(cod))
            assert cod in self.__errors_code, "'%s' não foi encontrado" % str(cod)

            return self.__errors_code[cod]

        except AssertionError as a:
            print(a.__repr__())
            return none_error
        except Exception as e:
            print(e.__repr__())
            return none_error
