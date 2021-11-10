from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

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


@driver.route('/setup')
@confirm_required
@login_required
def setup_drive():
    return render_template("Driver/setup.html")