from geopy import Nominatim, GoogleV3
from geopy.distance import geodesic
from config import Config


nom = Nominatim(user_agent="podvezisoseda, school project")
gv3 = GoogleV3(api_key=Config.api_key, domain='maps.google.ru')


def get_geocode_gv3(usplace):
    '''Геокодер корпорации зла Google, возвращает географические координаты объекта по его адресу'''
    try:
        return gv3.geocode(usplace)
    except:
        return None


def get_geocode_osm(usplace):
    '''Геокодер osm, возвращает географические координаты объекта по его адресу'''
    try:
        return nom.geocode(usplace)
    except:
        return None


def gd_distance(a, b):
    '''Расстояние между двумя точками в км с точностью до тысячных'''
    return round(geodesic(a, b).km * 1000) / 1000