# Конфигурация для разработки или продакшена. На сервере указать ProductionConfig!!!
export APP_SETTINGS="config.DevelopmentConfig"

# Пароли и конф. данные
export SECRET_KEY=''

export DATABASE_URI='postgresql+psycopg2://[ЛОГИН]:[ПАРОЛЬ]@[IP АДРЕС ИЛИ LOCALHOST]:[ПОРТ]/[ИМЯ БД]'

export EMAIL_LOGIN=''
export EMAIL_PASSWORD=''

export GOOGLE_MAPS_API_KEY=''


# Email адрес админа (для входа в админ-панель)
export ADMIN_EMAIL=''


# Переменная для использования команды flask, показывает, что main.py - главный файл запуска всего приложения
# Добавляет возможность прописать к db миграции
export FLASK_APP=manage.py


# Активация вирутального окружения python
source env/bin/activate
