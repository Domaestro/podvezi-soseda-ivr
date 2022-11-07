# Результаты тестирования
# .
# ----------------------------------------------------------------------
# Ran 1 test in 0.000s

# OK

import unittest
from geopy import Nominatim
from geopy.distance import geodesic


def gd_distance(a, b):
    '''Расстояние между двумя точками в км с точностью до тысячных'''
    return round(geodesic(a, b).km * 1000) / 1000


class TestGeocodeOSM(unittest.TestCase):
    '''Тестирование функции геокодирования по адресу'''
    def test_area(self):
        '''Проверка значений на эквивалентность'''
        self.assertEqual(gd_distance((55.75200715,37.63745695),(55.5440746,37.48187802923967)), 25.137)