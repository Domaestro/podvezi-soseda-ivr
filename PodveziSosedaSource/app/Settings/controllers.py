from flask import Blueprint, render_template, request, redirect, url_for, flash, session
from flask_login import login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash

from app.models import db, Users, Profiles
from app.utils.geoloc import get_geocode_gv3, get_geocode_osm


settings_module = Blueprint('settings', __name__, url_prefix ='/settings')



@settings_module.route("/", methods=["POST", "GET"])
@login_required
def settings():
    '''Настройки'''
    user = Users.query.filter(Users.id == current_user.get_id()).first()
    profile = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()
    return render_template("Settings/settings.html", first_name=user.first_name, second_name=user.second_name, email=user.email,
        phone=user.phoneNum, description=profile.description, address=profile.home_address, search_radius=profile.trip_search_radius, hidden="d-none" if user.confirmed == True else "0")


@settings_module.route('/upload_avatar', methods=["POST", "GET"])
@login_required
def upload():
    '''Загрузка аватара'''
    if request.method == 'POST':
        file = request.files['file']
        if file and current_user.verifyExt(file.filename):
            try:
                img = file.read()
                Profiles.query.filter(Profiles.user_id == current_user.get_id()).first().photo = img
                db.session.commit()

                flash("Аватар обновлен", "success")
            except FileNotFoundError as e:
                flash("Ошибка чтения файла", "error")
        else:
            flash("Ошибка обновления аватара", "error")
 
    return redirect("/settings")


@settings_module.route('/upload_new_password', methods=["POST", "GET"])
@login_required
def upload_new_password():
    '''Изменение пароля'''
    user = Users.query.filter(Users.id == current_user.get_id()).first()
    if request.method == 'POST':
        if len(request.form['new_psw']) > 4:
            if check_password_hash(user.psw, request.form['old_psw']): 
                try:
                    hash = generate_password_hash(request.form['new_psw'])
                    user.psw = hash
                    db.session.commit()
                    flash("Пароль успешно изменен", "success")
                except:
                    db.session.rollback()
                    flash("Ошибка изменения пароля", "error")
            else:
                flash("Пароль неверный", "error")
        else: flash("Новый пароль слишком короткий", "error")
    
    return redirect(url_for('settings.settings'))


@settings_module.route('/upload_basic_info', methods=["POST", "GET"])
@login_required
def upload_basic_info():
    '''Загрузка и обновление информации из профиля'''
    u = Users.query.filter(Users.id == current_user.get_id()).first()

    if request.method == 'POST':
        first_name = request.form["first_name"]
        second_name = request.form["second_name"]
        phone = request.form["phone"]
        email = request.form["email"]
        print(first_name, second_name, phone, email)
        try:
            if (first_name != u.first_name): u.first_name = first_name 
            if (second_name != u.second_name): u.second_name = second_name 
            if (phone != u.phoneNum): u.phoneNum = phone
            if (email != u.email):
                u.email = email
                u.confirmed = False
            db.session.commit()
            flash("Данные сохранены", "success")
            return redirect(url_for('send_confirm'))
        except:
            flash("Ошибка сохранения данных", "error") 

    return redirect("/settings")


@settings_module.route('/upload_description', methods=["POST", "GET"])
@login_required
def upload_desc():
    '''Загрузка описания профиля'''
    if request.method == 'POST':
        desc = request.form["desc"]
        if len(desc) <= 600:
            try:
                Profiles.query.filter(Profiles.user_id == current_user.get_id()).first().description = desc
                db.session.commit()
                flash("Описание обновлено", "success")
            except:
                flash("Ошибка обновления описания", "error")
        else:
            flash("Слишком длинное описание", "error")
 
    return redirect("/settings")


@settings_module.route('/address/confirm', methods=["POST", "GET"])
@login_required
def address_confirm():
    '''Подтверждение гео. адреса'''
    if request.method == 'POST':
        place = request.form["place"]
        #location = get_geocode_gv3(place) # определить адрес, используя Google
        location = get_geocode_osm(place) # определить адрес, используя Nominatim (Свободная лицензия, возможность установить на свой сервер)
        session["place"] = place
        if location:
            return render_template("Settings/address-confirm.html", address=location.address)
        else:
            flash("Вы ввели несуществующий адрес", "error")
 
    return redirect("/settings")


@settings_module.route('/address/upload', methods=["POST", "GET"])
@login_required
def address_upload():
    '''Загрузка гео. адреса'''
    if request.method == 'POST':
        place = session["place"]
        #location = get_geocode_gv3(place) # определить адрес, используя Google
        location = get_geocode_osm(place) # определить адрес, используя Nominatim (Свободная лицензия, возможность установить на свой сервер)
        print("Адрес"+location.address)
        if location:
            try:
                p = Profiles.query.filter(Profiles.user_id == current_user.get_id()).first()
                p.home_address = location.address
                p.home_latitude = location.latitude
                p.home_longitude = location.longitude
                db.session.commit()
                flash("Адрес загружен", "success")
            except:
                flash("Ошибка загрузки адреса", "error")

            return redirect("/settings")
        else:
            flash("Вы ввели несуществующий адрес, попробуйте указать его точнее", "error")
 
    return redirect("/settings")


@settings_module.route('/radius_change', methods=["POST", "GET"])
@login_required
def radius_change():
    '''Изменение радиуса поиска поездки'''
    if request.method == 'POST':
        radius = float(request.form["radius"])
        if 0.3 <= radius <= 3.0:
            try:
                Profiles.query.filter(Profiles.user_id == current_user.get_id()).first().trip_search_radius = radius
                db.session.commit()
                flash("Радиус поиска поездки изменён", "success")
            except:
                flash("Ошибка обновления радиуса поиска поездки", "error")
        else:
            flash("Некорректный радиус", "error")
 
    return redirect("/settings")