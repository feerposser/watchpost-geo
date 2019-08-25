class GeocodeNotTrusted(Exception):
    pass


class GeocodeNotFound(Exception):
    pass


class CityNotInDB(Exception):
    pass


class NoLatLng(Exception):
    pass


class InvalidReportFrom(Exception):
    pass


class IsNotModelCidadeOrIdError(Exception):
    pass


class NoCityFound(Exception):
    pass


class NeighborhoodNotInDB(Exception):
    pass


class NeighborhoodOrStreetNotSetup(Exception):
    pass


class NeighborhoodNotFound(Exception):
    pass


class MaxDistanceNeighborhoodNotFound(Exception):
    pass


class NeighborhoodNotInCity(Exception):
    pass


class ParamNotAcceptable(Exception):
    pass


class ParamCityEmpty(Exception):
    pass


class ParamNeighborhoodEmpty(Exception):
    pass


class NeighborhoodGeocodeNotFound(Exception):
    pass


class NeighborhoodOutsideCity(Exception):
    pass


class NotRighNeighborhood(Exception):
    pass


class CreateNeighborhoodError(Exception):
    pass


class CreateBlackListError(Exception):
    pass