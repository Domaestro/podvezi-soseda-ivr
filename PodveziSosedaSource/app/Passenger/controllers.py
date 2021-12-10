from flask import Blueprint, render_template, redirect,request, session, flash, make_response, url_for
from flask_login import login_required, current_user
import json

from datetime import date, timedelta, datetime

from app.models import db, Users, Profiles, Trips
from app.utils.utils import confirm_required
from app.utils.geoloc import get_geocode_osm, gd_distance


passenger = Blueprint('passenger', __name__, url_prefix ='/join')


@passenger.route('/')
@confirm_required
@login_required
def join():
    return render_template("Passenger/join.html")