from alg_utils.watchpost_exceptions import NoLatLng
from alg_utils.watchpost_geo_errors_cod import ErrorsCode

from blacklist.models import ModelBlackList


class Report:

    def __init__(self):
        self.report = {
            'RESULT': {
                'geocode': {'lat': 0, 'lng': 0},
                'input_address': {'country': 'Brasil', 'state': 'RS', 'city': '', 'neighborhood': '', 'street': '',
                                  'number': ''},
                'search_address': "",
                'confidence': []
            },
            'ERRORS': []
        }

    def merge_reports(self, report):
        self.merge_report_errors(report)
        self.add_result_geocode(report['RESULT']['geocode']['lat'], report['RESULT']['geocode']['lng'])
        self.report['RESULT']['confidence'] += report['RESULT']['confidence']
        if 'BLACKLIST' in report:
            self.report['BLACKLIST'] = report['BLACKLIST']

    def merge_report_errors(self, report):
        """
        Realiza um merge de um dict do formato padrão do report com a instancia atual de report.
        :param report: dict do formato report
        :return:
        """
        try:
            assert isinstance(report, dict), "'repor' deve ser um 'dict'"
            assert 'ERRORS' in report, "índice 'ERRORS' não encontrado em 'report'"

            self.report['ERRORS'] += report['ERRORS']

        except AssertionError as a:
            print(a.__repr__())
        except Exception as e:
            print(e.__repr__())

    def add_blacklist(self, blacklist):
        try:
            assert isinstance(blacklist, ModelBlackList), "'blacklist' deve ser um objeto 'ModelBlackList"
            blacklist = blacklist.__dict__

            self.report['BLACKLIST'] = {"id": blacklist['id'], "status": blacklist['status']}
            self.report['RESULT']['confidence'].append(13)
        except AssertionError as a:
            print(a.__repr__())

    def get_report(self):
        return self.report

    def add_result_geocode(self, lat, lng):
        try:
            if lat and lng:
                self.report['RESULT']['geocode']['lat'] = lat
                self.report['RESULT']['geocode']['lng'] = lng
            else:
                raise NoLatLng('Parâmetro de latitude ou longitude vazios. lat: %s lng: %s' % (lat, lng))
        except NoLatLng as n:
            raise n
        except Exception as e:
            raise Exception('Erro desconhecido: %s' % repr(e))

    def get_result_geocode(self):
        return self.report['RESULT']['geocode']

    def add_result_input_address(self, **kwargs):
        if 'number' in kwargs:
            self.report['RESULT']['input_address']['number'] = kwargs['number']
        if 'street' in kwargs:
            self.report['RESULT']['input_address']['street'] = kwargs['street']
        if 'neighborhood' in kwargs:
            self.report['RESULT']['input_address']['neighborhood'] = kwargs['neighborhood']
        if 'city' in kwargs:
            self.report['RESULT']['input_address']['city'] = kwargs['city']
        if 'state' in kwargs:
            self.report['RESULT']['input_address']['state'] = kwargs['state']
        if 'country' in kwargs:
            self.report['RESULT']['input_address']['country'] = kwargs['country']

    def get_result_input_address(self):
        return self.report['RESULT']['input_address']

    def add_result_search_address(self, address):
        self.report["RESULT"]["search_address"] = address

    def get_result_search_address(self):
        return self.report["RESULT"]["search_address"]

    def get_result_confidence(self):
        return self.report['RESULT']['confidence']

    def add_result_confidence(self, cod, warning=""):
        try:
            assert cod in (10, 12, 14, 14, 15, 16, 0, 21, 22, 23), "'cod: %s' não é um código válido." % str(cod)

            self.report['RESULT']['confidence'].append(cod)
            if warning:
                self.report['RESULT']['confidence'].append(warning)
        except Exception as e:
            print(e.__repr__())

    def add_error(self, cod, args=()):
        """
        :param cod: código do erro
        :param args: tupla com os args do erro
        :return: none
        Salva o código, a descrição, o tipo de exceção e os argumentos da exceção
        """
        try:
            assert isinstance(cod, int), "'cod' deve ser 'int' e não '%s'" % str(type(cod))

            error_details = ErrorsCode().get_error(cod)

            if not args:
                self.report["ERRORS"].append([cod, error_details["description"]])
            else:
                self.report["ERRORS"].append([cod, args, error_details["description"]])

        except AssertionError as a:
            print(a.__repr__())
        except Exception as e:
            print(e.__repr__())

    def get_errors(self):
        return self.report['ERRORS']

