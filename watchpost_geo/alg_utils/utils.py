from geopy.distance import distance
from math import sqrt


def max_distance(bounds_northeast_lat, bounds_northeast_lng, bounds_southwest_lat, bounds_southwest_lng, metric='km'):
    """

    :param bounds_northeast_lat: direita em cima
    :param bounds_northeast_lng:
    :param bounds_southwest_lat: esquerda em baixo
    :param bounds_southwest_lng:
    :return:
    """
    if bounds_northeast_lat and bounds_northeast_lng and bounds_southwest_lat and bounds_southwest_lng:
        if metric == 'km':
            return distance((bounds_northeast_lat, bounds_northeast_lng),
                            (bounds_southwest_lat, bounds_southwest_lng)).km
        elif metric == 'm':
            return distance((bounds_northeast_lat, bounds_northeast_lng),
                            (bounds_southwest_lat, bounds_southwest_lng)).m
        else:
            return None
