from flask import Blueprint, render_template, redirect,request, session, flash, make_response, url_for
from flask_login import login_required, current_user
import json

from datetime import date, timedelta, datetime

from app.models import db, Users, Profiles, Trips
from app.utils.utils import confirm_required
from app.utils.geoloc import get_geocode_osm, gd_distance
from .alchemyToJSON import AlchemyEncoder


passenger = Blueprint('passenger', __name__, url_prefix ='/join')


@passenger.route("/", methods=["GET", "POST"])
@confirm_required
@login_required
def join():
    # Пагинация (бесконечный скролл)
    POSTS_ON_PAGE = 3

    trips = Trips.query.filter(Trips.driver_id!=current_user.get_id(), Trips.trip_date>=datetime.now().date()).order_by(Trips.trip_date).all()

    # Проверка поездок на близость к дому точки выезда или точки приезда
    profile = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()
    home_lati = profile.home_latitude
    home_long = profile.home_longitude

    # В каком радиусе искать поездки (км)
    TRIP_RADIUS = profile.trip_search_radius

    valid_trips = []
    for trp in trips:
        driver = Users.query.filter(Users.id==trp.driver_id).first()
        drvr_prfl = Profiles.query.filter(Users.id==trp.driver_id).first()
        if gd_distance( (trp.from_latitude, trp.from_longitude ), (home_lati, home_long) ) <= TRIP_RADIUS or \
            gd_distance( (trp.to_latitude, trp.to_longitude ), (home_lati, home_long) ) <= TRIP_RADIUS:
                vtrip = {
                    "trip_id": trp.trip_id,
                    "driver_id": trp.driver_id,
                    "driver_name": f"{driver.first_name}", #{driver.second_name}",
                    "trip_type": "домой" if (drvr_prfl.home_latitude == trp.to_latitude and drvr_prfl.home_longitude == trp.to_longitude) else "в город",
                    "day": ["Сегодня", "Завтра", "Послезавтра"][trp.trip_date.day-datetime.now().date().day],
                    "time": trp.trip_time.strftime("%H:%M"),
                    "from": trp.from_address,
                    "to": trp.to_address,
                    "passengers": {
                        id: Users.query.filter(Users.id==id).first().first_name for id in trp.passengers_ids
                    },
                    "description": trp.description,
                    "joined": int(current_user.get_id()) in trp.passengers_ids
                }
                valid_trips.append(vtrip)

    if request.method == "POST":
        req = request.get_json()
        total_pages = len(valid_trips) // POSTS_ON_PAGE + 1
        resp = make_response(json.dumps({ "trips": valid_trips[POSTS_ON_PAGE*req['next_page']-POSTS_ON_PAGE+1:POSTS_ON_PAGE*req['next_page']], 
                                          "pages": total_pages }, cls=AlchemyEncoder))
        print(valid_trips[POSTS_ON_PAGE*req['next_page']-POSTS_ON_PAGE+1:POSTS_ON_PAGE*req['next_page']])                            
        return resp

    return render_template("Passenger/join.html", trips=valid_trips) # trips=valid_trips[0:POSTS_ON_PAGE]


@passenger.route("/<trip_id>", methods=["GET", "POST"])
@login_required
def join_trip(trip_id):
    trip = Trips.query.filter(Trips.trip_id==trip_id).first()
    if int(current_user.get_id()) in trip.passengers_ids:
        flash("Вы уже присоединились к этой поездке ранее", "error")
    elif len(trip.passengers_ids) >= trip.max_passengers_amount:
        flash("К поездке уже присоединилось максимальное количество пассажиров", "error")
    else:
        try:
            trip.passengers_ids = [*trip.passengers_ids, current_user.get_id()]
            flash("Вы успешно присоединились к поездке", "success")
            db.session.flush()
            db.session.commit()
        except:
            flash("Произошла ошибка", "error")
            db.session.rollback()
    return redirect(url_for("passenger.join"))


@passenger.route("/discard/<trip_id>", methods=["GET", "POST"])
@login_required
def discard_trip(trip_id):
    trip = Trips.query.filter(Trips.trip_id==trip_id).first()
    if int(current_user.get_id()) not in trip.passengers_ids:
        flash("Вы не присоединялись к этой поездке", "error")
    else:
        try:
            trip.passengers_ids = [int(i) for i in trip.passengers_ids if i != int(current_user.get_id())]
            flash("Вы успешно исключены из участников поездки", "success")
            db.session.flush()
            db.session.commit()
        except:
            flash("Произошла ошибка", "error")
            db.session.rollback()
    return redirect(url_for("passenger.join"))