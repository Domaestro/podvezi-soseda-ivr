import os

class Config(object):
    '''Объект, где хранятся все основные статические 
    переменные, необходимые для работы приложения'''

    # Определяет, включен ли режим отладки
    DEBUG = False

    # Включение защиты против "Cross-site Request Forgery (CSRF)"
    CSRF_ENABLED = True

    # Случайный ключ, которые будет исползоваться для подписи
    # данных, например cookies.
    SECRET_KEY = os.environ["SECRET_KEY"]

    # Настройки базы данных
    SQLALCHEMY_DATABASE_URI = os.environ["DATABASE_URI"]
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    SQLALCHEMY_ENGINE_OPTIONS = {"pool_pre_ping": True}  

    # Стиль админ-панели
    FLASK_ADMIN_SWATCH = "flatly"
    admin_login = os.environ["ADMIN_EMAIL"]

    # Максимальный объем передаваемых файлов
    MAX_CONTENT_LENGTH = 2048*2048

    # Директория static файлов
    #STATICFILES_DIRS = (os.path.join(os.path.abspath(os.path.dirname(__file__)), "Static"))


    # Настройки для отправки писем подтверждения
    domain = os.environ["SERVER_DOMAIN"]
    email_login = os.environ["EMAIL_LOGIN"]
    email_password = os.environ["EMAIL_PASSWORD"]

    # API ключ к Google Maps
    api_key = os.environ["GOOGLE_MAPS_API_KEY"]


class ProductionConfig(Config):
    '''Объект-наследник основного конфигурационного объекта, 
    предназначен для работы в конфига в продакшене'''
    DEBUG = False


class DevelopmentConfig(Config):
    '''Объект-наследник основного конфигурационного объекта,
     предназначен для работы в конфига во время разработки'''
    DEVELOPMENT = True
    DEBUG = True