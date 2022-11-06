from flask import Blueprint, render_template, redirect, url_for, session
from flask_login import login_required, current_user
from itsdangerous import SignatureExpired

from app.models import db, Users, Email_Confirm_Tokens
from app.utils.utils import confirm_required, secure_token


confirmEmail = Blueprint('confirmEmail', __name__, url_prefix ='/confirm_email')


@confirmEmail.route('/<token>')
def confirm_email(token):
    '''Подтверждение адреса email по токену'''
    try:
        user_id = Email_Confirm_Tokens.query.filter(token==token).all()[-1].user_id
        user_email = Users.query.filter(Users.id == user_id).first().email
        if user_email != session["email"]:
            return render_template("Confirm_Email/confirm_email_token.html", text="Токен недействителен", isOk=False)
        Email_Confirm_Tokens.query.filter(token==token).all()[-1].used = True

        secure_token.loads(token, salt='email-confirm', max_age=600) # max_age - время жизни токена в секундах       
        #Здесь делаем запись в бд, что пользователь подвердил адрес
        print("Пользователь подтвердил email " + session["email"])
        Users.query.filter(Users.email == session["email"]).first().confirmed = True
        db.session.flush()
        db.session.commit()
        return redirect(url_for('/profile'))
    except SignatureExpired:
        return render_template("Confirm_Email/confirm_email_token.html", text = "Ваша ссылка истекла, запросите новую", isOk=False)
    except:
        db.session.rollback()
        if "email" not in session:
            return render_template("Confirm_Email/confirm_email_token.html", text="Произошла ошибка, попробуйте позже", isOk=False)
    return render_template("Confirm_Email/confirm_email_token.html", text="Успешно подтвержден адрес:", email=session["email"], isOk=True) 


@confirmEmail.route('/letter')
def confirm_letter():
    '''Информация об отправке письма на почту'''
    email = Users.query.filter(Users.id == current_user.get_id()).first().email
    return render_template("Confirm_Email/confirm_email_letter.html", email=email) #'Вам на почту отправлена ссылка, перейдите по ней, чтобы подтвердить свой адрес электронной почты'


# Представление для отправки письма на почту с подтверждением, если пользователь не подтвержден, используется декоратор, если подтвержден, идет в профиль
@confirmEmail.route("/send_confirm")
@confirm_required
@login_required
def send_confirm():
    '''Ссылка в настройки'''
    return redirect(url_for('settings'))