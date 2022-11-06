import os
from flask import Flask

from .database import db, migrate
from .admin import admin

# Вызов блюпринтов
import app.General.controllers as generalModule
import app.AuthModule.controllers as authModule
import app.ConfirmEmail.controllers as confirmEmailModule
import app.Profile.controllers as profileModule
import app.Settings.controllers as settingsModule
import app.Driver.controllers as driverModule
import app.Passenger.controllers as passengerModule


def create_app():
    '''Основная функция по инициализации всего приложения,
    осуществляет подключение к базе данных и регистрирует
    все модули основного функционала веб-приложения'''

    app = Flask(__name__)
    app.config.from_object(os.environ['APP_SETTINGS'])

    db.init_app(app)
    with app.test_request_context():
        db.create_all()

    migrate.init_app(app, db)
    admin.init_app(app)

    # Регистрация блюпринтов
    app.register_blueprint(generalModule.general)
    app.register_blueprint(authModule.auth)
    app.register_blueprint(confirmEmailModule.confirmEmail)
    app.register_blueprint(profileModule.profiles)
    app.register_blueprint(settingsModule.settings_module)
    app.register_blueprint(driverModule.driver)
    app.register_blueprint(passengerModule.passenger)

    # Устанавливаем логин менеджер
    authModule.login_manager.init_app(app)


    return app