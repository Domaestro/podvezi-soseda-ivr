from flask import Blueprint, render_template, request, redirect, url_for, flash
from flask_login import LoginManager, login_user, login_required, current_user, logout_user
from werkzeug.security import generate_password_hash, check_password_hash


from app.models import db, Users, Profiles
from app.utils.userLogin import UserLogin


# Подключим модуль авторизации Flask-login
login_manager = LoginManager()
# Перенаправляем неавторизованного пользователя на страницу авторизации при попытке посетить закрытую страницу
login_manager.login_view = 'auth.login'
login_manager.login_message = "Авторизуйтесь для доступа к закрытым страницам"
login_manager.login_message_category = "success"

@login_manager.user_loader
def load_user(user_id):
    return UserLogin().fromDB(user_id, Users)


auth = Blueprint('auth', __name__, url_prefix ='/auth')


@auth.route("/register", methods=("POST", "GET"))
def register():
    # Если пользователь уже вошел, он идет в свой профиль
    if current_user.is_authenticated:
        return redirect("/profile")

    if request.method == "POST":
        # Проверка пароля на сложность
        if len(request.form['psw']) < 5:
             flash('Пароль должен быть длиннее пяти символов', category = 'error')
             return render_template("Auth/register.html", title="Регистрация")

        # Создание нового пользователя
        try:
            hash = generate_password_hash(request.form['psw'])
            email = request.form['email']

            u = Users(email=email, psw=hash, first_name=request.form['first_name'], second_name=request.form['second_name'],
                phoneNum=request.form['phoneNum'])
            db.session.add(u)
            db.session.flush()

            p = Profiles(user_id = u.id)
            db.session.add(p)
            db.session.commit()

            print("Данные внесены в бд")

            # Осуществляем логин пользователя
            user = Users.query.filter(Users.email == email).first()
            if user:
                userlogin = UserLogin().create(user)
                login_user(userlogin, remember=True)
            print("Вход в аккаунт выполнен")

            return redirect(url_for('confirmEmail.send_confirm'))
        except Exception as exc:
            print(exc)
            db.session.rollback()
            flash('Не удалось зарегистрироваться', category = 'error')
            print("Ошибка добавления в БД")

    return render_template("Auth/register.html", title="Регистрация")


@auth.route("/login", methods=["POST", "GET"])
def login():
    # Если пользователь уже вошел, он идет в свой профиль
    if current_user.is_authenticated:
        return redirect("/profile")

    if request.method == "POST":
        user = Users.query.filter(Users.email == request.form['email']).first()
        if user and check_password_hash(user.psw, request.form['psw']):
            userlogin = UserLogin().create(user)
            rm = True if request.form.get('remainme') else False # Запоминать пользователя или нет
            login_user(userlogin, remember=rm)
            return redirect(request.args.get("next") or "/profile")

        flash("Неверная пара логин/пароль", "error")
 
    return render_template("Auth/login.html", title="Авторизация")


@auth.route('/logout')
@login_required
def logout():
    logout_user()
    flash("Вы вышли из аккаунта", "success")
    return redirect(url_for('.login'))