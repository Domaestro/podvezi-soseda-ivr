from flask import Blueprint, render_template, redirect, url_for
from flask_login import login_required, current_user
from itsdangerous import SignatureExpired

from app.models import db, Users
from app.utils.utils import confirm_required, secure_token, cur_user

confirmEmail = Blueprint('confirmEmail', __name__, url_prefix ='/confirm_email')


@confirmEmail.route('/<token>')
def confirm_email(token):
    try:
        secure_token.loads(token, salt='email-confirm', max_age=600) # max_age - время жизни токена в секундах       
        # Здесь делаем запись в бд, что пользователь подвердил адрес
        print("Пользователь подтвердил email " + cur_user.email)
        Users.query.filter(Users.email == cur_user.email).first().confirmed = True
        db.session.flush()
        db.session.commit()
        return redirect(url_for('/profile'))
    except SignatureExpired:
        return render_template("Confirm_Email/confirm_email_token.html", text = "Ваша ссылка истекла, запросите новую")
    except:
        db.session.rollback()
        if cur_user.email == None:
            return render_template("Confirm_Email/confirm_email_token.html", text="Произошла ошибка, попробуйте позже")
    return render_template("Confirm_Email/confirm_email_token.html", text="Успешно подтвержден адрес:", email=cur_user.email) 


@confirmEmail.route('/letter')
def confirm_letter():
    email = Users.query.filter(Users.id == current_user.get_id()).first().email
    return render_template("Confirm_Email/confirm_email_letter.html", email=email) #'Вам на почту отправлена ссылка, перейдите по ней, чтобы подтвердить свой адрес электронной почты'


# Представление для отправки письма на почту с подтверждением, если пользователь не подтвержден, используется декоратор, если подтвержден, идет в профиль
@confirmEmail.route("/send_confirm")
@confirm_required
@login_required
def send_confirm():
    return redirect(url_for('settings'))