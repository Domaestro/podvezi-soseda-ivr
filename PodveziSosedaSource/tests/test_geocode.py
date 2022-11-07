# Результаты тестирования
# .
# ----------------------------------------------------------------------
# Ran 1 test in 1.207s

# OK

import unittest
from geopy import Nominatim, GoogleV3
from geopy.distance import geodesic


nom = Nominatim(user_agent="podvezisoseda, school project")

def get_geocode_osm(usplace):
    '''Геокодер osm, возвращает географические координаты объекта по его адресу'''
    try:
        return nom.geocode(usplace)
    except:
        return None


address_request = ["Москва, Солянка 14а", "Москва, бунинские луга, д4", "Москва, Кремль"]
address_response =["14А с3, улица Солянка, Таганский район, Москва, Центральный федеральный округ, 109074, Россия", 
                    "Жилой квартал «Бунинские луга», Коммунарка, поселение Сосенское, Москва, Центральный федеральный округ, 142770, Россия",
                    "Кремль, Северо-Восточная хорда, Кусково, район Вешняки, Москва, Центральный федеральный округ, 109456, Россия"]
class TestGeocodeOSM(unittest.TestCase):
    '''Тестирование функции геокодирования по адресу'''
    def test_area(self):
        '''Проверка значений на эквивалентность'''
        for i in range(len(address_request)):
            self.assertEqual(get_geocode_osm(address_request[i]).address, address_response[i])