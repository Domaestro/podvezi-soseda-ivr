from flask import Blueprint, render_template, url_for, make_response, current_app
from flask_login import login_required, current_user

from app.models import Users, Profiles
from app.utils.utils import confirm_required


profiles = Blueprint('profiles', __name__, url_prefix ='/profile')


# Профиль вошедшего пользователя

@profiles.route("/", methods=["POST", "GET"])
@confirm_required
@login_required
def profile():
    '''Профиль пользователя'''
    user = Users.query.filter(Users.id == current_user.get_id()).first()
    profile = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()
    return render_template("Profile/profile.html", id=current_user.get_id(), name =f"{user.first_name} {user.second_name}", description=profile.description, email=user.email, 
        phone=user.phoneNum, confirmed=user.confirmed, address=profile.home_address)


@profiles.route('/load_avatar')
@login_required
def load_avatar():
    '''Выгрузка аватара из бд'''
    profile = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()

    img = None
    if not profile.photo:
        try:
            with current_app.open_resource(current_app.root_path + url_for('static', filename='imgs/default-ava.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: "+str(e))
    else:
        img = profile.photo

    if not img:
        return ""
    h = make_response(img)
    return h


# Профили остальных пользователей

@profiles.route("/<user_id>")
@login_required
def user(user_id):
    '''Профиль внешнего пользователя'''
    user = Users.query.filter(Users.id == user_id).first_or_404()
    profile = Profiles.query.filter(Profiles.user_id == user_id).first_or_404()
    return render_template("Profile/user.html", id=user_id, name =f"{user.first_name} {user.second_name}", description=profile.description, email=user.email, 
        phone=user.phoneNum, confirmed=user.confirmed, address=profile.home_address)


@profiles.route('/load_user_avatar/<user_id>')
@login_required
def load_user_avatar(user_id):
    '''Выгрузка аватара из бд'''
    profile = Profiles.query.filter(Profiles.user_id == user_id).first_or_404()

    img = None
    if not profile.photo:
        try:
            with current_app.open_resource(current_app.root_path + url_for('static', filename='imgs/default-ava.png'), "rb") as f:
                img = f.read()
        except FileNotFoundError as e:
                print("Не найден аватар по умолчанию: "+str(e))
    else:
        img = profile.photo

    if not img:
        return ""
    h = make_response(img)
    return h