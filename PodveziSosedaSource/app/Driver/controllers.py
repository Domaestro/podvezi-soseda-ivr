from flask import Blueprint, render_template, redirect,request, session, flash, make_response, url_for
from flask_login import login_required, current_user
import json

from datetime import date, timedelta, datetime

from app.models import db, Users, Profiles, Trips
from app.utils.utils import confirm_required
from app.utils.geoloc import get_geocode_osm, gd_distance
from .alchemyToJSON import AlchemyEncoder

driver = Blueprint('driver', __name__, url_prefix ='/drive')


@driver.route('/')
@confirm_required
@login_required
def drive():
    '''Страница водителя'''
    first_2_actual_trips = Trips.query.filter(Trips.driver_id == current_user.get_id(), Trips.trip_date>=datetime.now().date()) \
                                .order_by(Trips.trip_date).limit(2).all()
    days_possible=["Сегодня", "Завтра", "Послезавтра"]
    days=[days_possible[first_2_actual_trips[i].trip_date.day-datetime.now().date().day] for i in range(len(first_2_actual_trips))]

    last_2_in_history = Trips.query.filter(Trips.driver_id == current_user.get_id(), Trips.trip_date<datetime.now().date()) \
                                .order_by(Trips.trip_date.desc()).limit(2).all()

    return render_template("Driver/driver.html", trips=first_2_actual_trips, days=days, history=last_2_in_history)


@driver.route('/setup', methods=["GET", "POST"])
@confirm_required
@login_required
def setup_drive():
    '''Страница для создания новой поездки'''
    # Проверка заполненности профиля у пользователя
    profile = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()
    if not profile.home_address:
        flash("Вы не указали домашний адрес в профиле", "error")
        return redirect(url_for("driver.drive"))

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

        # Получение данных из формы
        trip_type = int(request.form["tripType"])
        address = get_geocode_osm(request.form["addressAuto"])
        day_delta = int(request.form["day"])-1 # Через сколько дней будет поездка
        time_raw = request.form["timeRaw"]
        passengers = int(request.form["passengersNum"])
        description = request.form["tripDescription"]

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
        trip_time = trip_datetime.time()
        passengers_number = passengers

        #print(f'Создана новая поездка \nОткуда: {address_from}\nКуда: {address_to}\nДата поездки: {trip_date}\nВремя поездки: {trip_datetime}\nМаксимальное число пассажиров: {passengers_number}')

        # Проверка, не насоздавал ли пользователь слишком много поездок
        look_for_trips = Trips.query.filter(Trips.trip_date==trip_date, Trips.driver_id==current_user.get_id()).all()
        #look_for_trips = Trips.query.filter( Trips.driver_id==current_user.get_id()).all()
        if len(look_for_trips) > 2:
            flash("Запрещено создавать больше трех поездок на один день", "error")
            return redirect(url_for("driver.drive"))

        # Проверка этой новой поездки на схожесть с уже существующими
        same_date_trips = Trips.query.filter(Trips.trip_date==trip_date).all()
        for trp in same_date_trips:
            if gd_distance( (trp.from_latitude, trp.from_longitude ), (from_lati, from_long) ) < 0.6 and \
               gd_distance( (trp.to_latitude, trp.to_longitude ), (to_lati, to_long) ) < 0.6 and \
               trp.trip_time.hour==trip_time.hour and \
               abs(trp.trip_time.minute-trip_time.minute) < 30:

                driver = Users.query.filter(Users.id==trp.driver_id).first()
                if driver: 
                    driver_name = driver.first_name+" "+driver.second_name
                    driver_link = url_for("profiles.user", user_id=driver.id)

                session["rawTime"]=time_raw
                session["tripDescription"]=description
                return render_template("Driver/similar.html",
                                      from_where=trp.from_address, 
                                      to_where=trp.to_address,
                                      date=trp.trip_date, 
                                      time=f'{trp.trip_time.hour}:{trp.trip_time.minute}', 
                                      driver_link=driver_link, 
                                      driver_name=driver_name)

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
                          trip_date=trip_date,
                          trip_time=trip_time,
                          description=description)
            db.session.add(trips)
            db.session.flush()
            db.session.commit()

            flash("Поездка успешно создана", "success")

            # Обнуление сессии
            session["radioChecked"] = 0
            session["address"] = ""
            session["tripDayNum"] = 0
            session["rawTime"] = ""
            session["passengersValue"] = 0

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
    '''Страница с картой'''
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


# Создание поездки, даже если уже есть похожая
@driver.route("/force", methods=["GET"])
@confirm_required
@login_required
def create_trip_by_force():
    # Получение данных, сохраненных в сессии
    trip_type = int(session["radioChecked"])
    address = get_geocode_osm(session["address"])
    day_delta = int(session["tripDayNum"]) # Через сколько дней будет поездка
    time_raw = session["rawTime"]
    passengers = int(session["passengersValue"])
    description = session["tripDescription"]

    # Преобразование данных

    profile = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()

    if trip_type == 1 or trip_type == 0:
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
    trip_time = trip_datetime.time()
    if passengers==0:
        passengers_number = 1 
    else:
        passengers_number = passengers+1

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
                        trip_date=trip_date,
                        trip_time=trip_time,
                        description=description)
        db.session.add(trips)
        db.session.flush()
        db.session.commit()

        flash("Поездка успешно создана", "success")

        # Обнуление сессии
        session["radioChecked"] = 0
        session["address"] = ""
        session["tripDayNum"] = 0
        session["rawTime"] = ""
        session["passengersValue"] = 0

    except Exception as exc:
        print(exc)
        db.session.rollback()
        flash('Не удалось создать поездку', category = 'error')
        print("Ошибка добавления поездки в бд")
    
    return redirect(url_for("driver.drive"))


@driver.route("/active_trips", methods=["GET"])
@confirm_required
@login_required
def active_trips():
    '''Список предстоящих поездок'''
    actual_trips = Trips.query.filter(Trips.driver_id == current_user.get_id(), Trips.trip_date>=datetime.now().date()) \
                                .order_by(Trips.trip_date).all()
    days_possible = ["Сегодня", "Завтра", "Послезавтра"]
    days = [days_possible[actual_trips[i].trip_date.day - datetime.now().date().day] for i in range(len(actual_trips))]
    return render_template("Driver/active_trips.html", trips=actual_trips, days=days)


@driver.route("/trip/<trip_id>", methods=["GET"])
@login_required
def trip(trip_id):
    '''Отдельная поездка'''
    trip = Trips.query.filter(Trips.driver_id == current_user.get_id(), Trips.trip_id==trip_id) \
                .first_or_404()

    future_trip = None

    if trip.trip_date>=datetime.now().date():
        date = ["Сегодня", "Завтра", "Послезавтра"][trip.trip_date.day-datetime.now().date().day]
        future_trip = True
    else:
        date = trip.trip_date.strftime(r"%d.%m.%Y")
        future_trip = False

    passengers = {}
    if trip.passengers_ids:
        for p_id in trip.passengers_ids:
            user = Users.query.filter(Users.id==p_id).first()
            passengers[p_id] = f'{user.first_name} {user.second_name}'
    
    return render_template("Driver/trip_full_info.html", trip=trip, date=date, passengers=passengers, future=future_trip)


@driver.route("/trip/change/<trip_id>", methods=["GET", "POST"])
@login_required
def change(trip_id):
    '''Изменение информации о поездке'''
    trip = Trips.query.filter(Trips.driver_id == current_user.get_id(), Trips.trip_id==trip_id, Trips.trip_date>=datetime.now().date()) \
                .first_or_404()

    if request.method == "POST":
        new_description = request.form["tripDescription"]

        try:
            trip.description = new_description
            db.session.commit()
            flash("Описание поездки обновлено", "success")
        except:
            db.session.rollback()
            flash("Ошибка", "error")

        return redirect(url_for("driver.drive"))

    date = ["Сегодня", "Завтра", "Послезавтра"][trip.trip_date.day-datetime.now().date().day]

    passengers = {}
    if trip.passengers_ids:
        for p_id in trip.passengers_ids:
            user = Users.query.filter(Users.id==p_id).first()
            passengers[p_id] = f'{user.first_name} {user.second_name}'
    
    return render_template("Driver/trip_change.html", trip=trip, date=date, passengers=passengers)


@driver.route("/history", methods=["GET", "POST"])
@confirm_required
@login_required
def history():
    '''История поездок'''

    # Пагинация (бесконечный скролл)
    POSTS_ON_PAGE = 3

    if request.method == "POST":
        req = request.get_json()
        more_history = Trips.query.filter(Trips.driver_id == current_user.get_id(), Trips.trip_date<datetime.now().date()) \
                                .order_by(Trips.trip_date.desc())
        paginated_history = more_history.paginate(req['next_page'], POSTS_ON_PAGE, False).items
        total_pages = more_history.count() // POSTS_ON_PAGE + 1
        
        resp = make_response(json.dumps({ "trips": paginated_history, "pages": total_pages }, cls=AlchemyEncoder))

        return resp

    history = Trips.query.filter(Trips.driver_id == current_user.get_id(), Trips.trip_date<datetime.now().date()) \
                                .order_by(Trips.trip_date.desc()).paginate(1, POSTS_ON_PAGE, False).items
    return render_template("Driver/history.html", trips=history)