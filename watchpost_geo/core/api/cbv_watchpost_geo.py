# -- Class-based Views do Watchpost-Geo
# As classes aqui são cbv, baseadas nas views do django, mas respondendo às solicitações e respostas do django rest
# Utilizadas para fazer as buscas de endereço e no final retornar um json personalizado. O viewset do django rest
# serve para manipular o banco de dados com as informações de cidades e bairros.
# https://www.django-rest-framework.org/api-guide/views/#class-based-views

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.authentication import TokenAuthentication

from core.report import Report
from core.manage_data import ManageCore
from alg_utils.watchpost_exceptions import GeocodeNotTrusted, ParamCityEmpty, ParamNeighborhoodEmpty, CityNotInDB, \
    NeighborhoodGeocodeNotFound, CreateNeighborhoodError, GeocodeNotFound, NeighborhoodOrStreetNotSetup


class WatchpostGeocode(APIView):
    permission_classes = [IsAuthenticated]
    authentication_classes = [TokenAuthentication]

    @staticmethod
    def clear_input_params(city, neighborhood):
        """
        Analisa os dados de cidade, bairro e tipo de requisição.
        :param city: cidade
        :param neighborhood: bairro
        :return:
        """
        try:
            if not city:
                raise ParamCityEmpty("Parâmetro 'city' vazio.")

            if not neighborhood:
                raise ParamNeighborhoodEmpty("Parâmetro 'neighborhood' vazio.")

        except ParamCityEmpty as p:
            print(p.__repr__())
            raise ParamCityEmpty(113)
        except ParamNeighborhoodEmpty as p:
            print(p.__repr__())
            raise ParamNeighborhoodEmpty(114)
        except Exception as e:
            print(e.__repr__())
            raise Exception(115)

    def get(self, request, format=None):
        report = Report()

        response_status = status.HTTP_202_ACCEPTED

        # print(request.user)
        # print(type(request.user))

        user = request.user
        neighborhood = request.query_params.get('neighborhood', None).upper()
        city = request.query_params.get('city', None).upper()
        street = request.query_params.get('street', None)
        number = request.query_params.get('number', None)

        report.add_result_input_address(city=city, neighborhood=neighborhood, street=street, number=number)

        try:
            self.clear_input_params(city, neighborhood)
        except ParamCityEmpty as p:
            report.add_error(p.args[0])
            return Response(report.report, status=status.HTTP_400_BAD_REQUEST)
        except ParamNeighborhoodEmpty as p:
            report.add_error(p.args[0])
            return Response(report.report, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            report.add_error(e.args[0])
            return Response(report.report, status=status.HTTP_400_BAD_REQUEST)

        try:
            manage_core = ManageCore(neighborhood=neighborhood, street=street, number=number, city=city, user=user)

            report.add_result_search_address(manage_core.formatted_address)

            if manage_core.city_exists(city):
                if manage_core.neighborhood_exists_in_city(city=manage_core.get_city_data(),
                                                           neighborhood=manage_core.neighborhood_name)[0]:
                    print('=================== BAIRRO PRESENTE:')
                    teste = manage_core.get_location()
                    report.merge_reports(teste)
                else:
                    print('=================== BAIRRO NÃO ENCONTRADO:')
                    geocode = manage_core.search_geocode_neighborhood()
                    if geocode:
                        print('......', geocode)
                        manage_core.__init__(neighborhood=neighborhood, street=street, number=number, city=city)
                        teste = manage_core.get_location()
                        report.merge_reports(teste)
                        reponse_status = status.HTTP_200_OK
                    else:
                        print("fazendo a busca sem garantias")
                        teste = manage_core.get_lat_lng(manage_core.get_geocode())
                        if teste:
                            report.add_result_geocode(teste['lat'], teste['lng'])
                            response_status = status.HTTP_200_OK
            else:
                raise CityNotInDB("Cidade '%s' não encontrada no banco de dados" % city)
        except NeighborhoodOrStreetNotSetup as n:
            print(331, n.__repr__())
            response_status = status.HTTP_400_BAD_REQUEST
            report.add_error(cod=311, args=n.args)
        except GeocodeNotFound as g:
            print('aaaaaa', g.__repr__())
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
        except CreateNeighborhoodError as c:
            print(121, c.__repr__())
            print('salvar blacklist')
            from cidades.manage_data import ManageCity
            from blacklist.manage_data import ManageBlackList
            blacklist = ManageBlackList.create_or_retrieve_blacklist(city=ManageCity(city).get_city_data(),
                                                                     neighborhood=neighborhood)
            report.add_blacklist(blacklist)
            response_status = status.HTTP_500_INTERNAL_SERVER_ERROR
            report.add_error(cod=121, args=c.args)
        except CityNotInDB as c:
            print(122, c.__repr__())
            response_status = status.HTTP_404_NOT_FOUND
            report.add_error(cod=122, args=c.args)
        except GeocodeNotTrusted as g:
            print(123, g.__repr__())
            response_status = status.HTTP_200_OK
            report.add_error(cod=123, args=g.args)
        except NeighborhoodGeocodeNotFound as n:
            print(124, n.__repr__())
            response_status = status.HTTP_404_NOT_FOUND
            report.add_error(cod=124, args=n.args)
        except Exception as e:
            print(125, e.__repr__())
            response_status = status.HTTP_400_BAD_REQUEST
            report.add_error(cod=125, args=e.args)
        finally:
            return Response(report.report, status=response_status)
