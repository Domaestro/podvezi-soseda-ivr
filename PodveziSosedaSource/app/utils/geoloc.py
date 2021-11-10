from geopy import GoogleV3
from config import Config


gv3 = GoogleV3(api_key=Config.api_key, domain='maps.google.ru')


def get_geocode(usplace):
    try:
        return gv3.geocode(usplace)
    except:
        return None