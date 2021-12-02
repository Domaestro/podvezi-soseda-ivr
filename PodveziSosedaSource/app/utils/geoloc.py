from geopy import Nominatim, GoogleV3
from geopy.distance import geodesic
from config import Config


nom = Nominatim(user_agent="podvezisoseda")
gv3 = GoogleV3(api_key=Config.api_key, domain='maps.google.ru')


def get_geocode_gv3(usplace):
    '''Геокодер корпорации зла Google, предпочтительно не использовать, но работает иногда лучше'''
    try:
        return gv3.geocode(usplace)
    except:
        return None


def get_geocode_osm(usplace):
    '''Геокодер от нормальных ребят из osm, использовать в первую очередь'''
    try:
        return nom.geocode(usplace)
    except:
        return None


def gd_distance(a, b):
    '''Расстояние между двумя точками в км с точностью до тысячных'''
    return round(geodesic(a, b).km * 1000) / 1000