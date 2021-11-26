from flask import Blueprint, render_template, request, session
from flask_login import login_required, current_user

from app.models import db, Users, Profiles
from app.utils.utils import confirm_required
from app.utils.geoloc import get_geocode


driver = Blueprint('driver', __name__, url_prefix ='/drive')


@driver.route('/')
@confirm_required
@login_required
def drive():
    user = Users.query.filter(Users.id == current_user.get_id()).first()
    return render_template("Driver/driver.html")


def set_sessions():
    '''Дефолтные значения переменным в сессии'''
    session_strings = ["address", "rawTime"]
    session_ints = ["radioChecked", "tripDayNum", "passengersValue"]
    for svalue in session_strings:   
        if svalue not in session:   
            session[svalue]=""
    for svalue in session_ints:
        if svalue not in session:
            session[svalue] = 0

@driver.route('/setup', methods=["GET", "POST"])
@confirm_required
@login_required
def setup_drive():
    # Создание переменных в сессии, в которых будет хранится информация из формы
    set_sessions()
    # Обработка формы
    if request.method == "POST":
        # Обнуление сессии
        session["radioChecked"] = 0
        session["address"] = ""
        session["tripDayNum"] = 0
        session["rawTime"] = ""
        session["passengersValue"] = 0
        # Сохранение данных в бд
        print("сохраняю созданную поездку")

    return render_template("Driver/setup.html")


@driver.route("/maps")
@confirm_required
@login_required
def maps():
    return render_template("Driver/maps.html")


@driver.route("/get_address_from_map", methods=["GET"])
@confirm_required
@login_required
def get_address_from_map():
    '''Сохраняет полученный адрес в сессии'''
    if request.method == "GET":
        session["address"] = request.args.get("address")
    return session["address"]


@driver.route("/get_form_input", methods=["GET"])
@confirm_required
@login_required
def get_form_input():
    '''Возвращает сохраненные данные из формы в виде json'''
    fields = {"address": session["address"],
              "radioChecked": session["radioChecked"],
              "tripDayNum": session["tripDayNum"],
              "rawTime": session["rawTime"],
              "passengersValue": session["passengersValue"]}
    return fields


@driver.route("/safe_form_input", methods=["GET"])
@confirm_required
@login_required
def safe_form_input():
    '''Сохраняет данные из формы в сессии'''
    session["radioChecked"] = int(request.args.get("triptype"))-1
    session["address"] = request.args.get("address") 
    session["tripDayNum"] = int(request.args.get("tripday"))-1
    session["rawTime"] = request.args.get("timeinput")
    session["passengersValue"] = int(request.args.get("passengers"))-1
    return "ok"