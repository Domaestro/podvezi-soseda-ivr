from flask import Blueprint, render_template, redirect,request, session, flash
from flask.helpers import url_for
from flask_login import login_required, current_user

from datetime import date, timedelta, datetime

from app.models import db, Users, Profiles, Trips
from app.utils.utils import confirm_required
from app.utils.geoloc import get_geocode_osm, gd_distance


driver = Blueprint('driver', __name__, url_prefix ='/drive')


@driver.route('/')
@confirm_required
@login_required
def drive():
    user = Users.query.filter(Users.id == current_user.get_id()).first()
    return render_template("Driver/driver.html")


@driver.route('/setup', methods=["GET", "POST"])
@confirm_required
@login_required
def setup_drive():
    # Создание переменных в сессии, в которых будет хранится информация из формы
    session_strings = ["address", "rawTime"]
    session_ints = ["radioChecked", "tripDayNum", "passengersValue"]
    for svalue in session_strings:   
        if svalue not in session:   
            session[svalue]=""
    for svalue in session_ints:
        if svalue not in session:
            session[svalue] = 0

    # Обработка формы
    if request.method == "POST":

        # Обнуление сессии
        session["radioChecked"] = 0
        session["address"] = ""
        session["tripDayNum"] = 0
        session["rawTime"] = ""
        session["passengersValue"] = 0

        # Получение данных из формы
        trip_type = int(request.form["tripType"])
        address = get_geocode_osm(request.form["addressAuto"])
        day_delta = int(request.form["day"]) # Через сколько дней будет поездка
        time_raw = request.form["timeRaw"]
        passengers = int(request.form["passengersNum"])

        # Преобразование данных
        profile = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()

        if trip_type == 1:
            # Домой
            address_from = address.address
            address_to = profile.home_address # Домашний адрес, указанный в профиле пользователя
            from_lati = address.latitude
            from_long = address.longitude
            to_lati = profile.home_latitude
            to_long = profile.home_longitude
        else:
            # В город
            address_from = profile.home_address # Домашний адрес, указанный в профиле пользователя
            address_to = address.address
            from_lati = profile.home_latitude
            from_long = profile.home_longitude
            to_lati = address.latitude
            to_long = address.longitude
        
        trip_date = date.today() + timedelta(days=day_delta)
        trip_datetime = datetime.strptime(f'{trip_date.day}/{trip_date.month}/{trip_date.year} {time_raw}', r'%d/%m/%Y %H:%M')
        passengers_number = passengers

        #print(f'Создана новая поездка \nОткуда: {address_from}\nКуда: {address_to}\nДата поездки: {trip_date}\nВремя поездки: {trip_datetime}\nМаксимальное число пассажиров: {passengers_number}')

        ####
        #### Проверка этой новой поездки на схожесть с уже существующими
        # similar_trips = Trips.query.filter( trip_datetime.date==Trips.trip_datetime.date \
        #                                     and (abs((trip_datetime-Trips.trip_datetime).hour) <= 1 and abs((trip_datetime-Trips.trip_datetime).minute) <= 30) \
        #                                     and gd_distance(from_lati, Trips.from_latitude) <= 0.5 \
        #                                     and gd_distance(to_lati, Trips.to_latitude) <= 0.5
        #                                )
        # similar_trips = Trips.query.filter(gd_distance((from_lati, from_long), (Trips.from_latitude, Trips.from_long)) <= 0.5).first()
        # Надо добавить hybrid фильтр в модель
        ####

        # Запись в бд
        try:
            trips = Trips(driver_id=current_user.get_id(), 
                          max_passengers_amount=passengers_number,
                          from_address=address_from,
                          from_latitude=from_lati,
                          from_longitude=from_long,
                          to_address=address_to,
                          to_latitude=to_lati,
                          to_longitude=to_long,
                          trip_datetime=trip_datetime
                          )
            db.session.add(trips)
            db.session.flush()
            db.session.commit()

        except Exception as exc:
            print(exc)
            db.session.rollback()
            flash('Не удалось создать поездку', category = 'error')
            print("Ошибка добавления поездки в бд")

        return redirect(url_for("driver.drive"))

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