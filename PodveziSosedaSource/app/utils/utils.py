from flask import redirect, url_for, flash, session
from itsdangerous import URLSafeTimedSerializer
from flask_login import current_user

from config import Config
from app.models import db, Users, Email_Confirm_Tokens
from .sendEmail import send_link


secure_token = URLSafeTimedSerializer(Config.SECRET_KEY) # Переменная для генерации токена подтверждения email

# Функция - декоратор на наличие confirmed = True пользователя
from functools import wraps
def confirm_required(func):
    @wraps(func)
    def wrapper():
        try:
            if Users.query.filter(Users.id == current_user.get_id()).first().confirmed: # Берем из базы данных значение из столбца confirmed
                return func()
            else:
                email = Users.query.filter(Users.id == current_user.get_id()).first().email
                token = secure_token.dumps(email, salt='email-confirm')

                # Сохраняем токен в базу данных
                t = Email_Confirm_Tokens(user_id=current_user.get_id(), token=token)
                db.session.add(t)
                db.session.flush()
                db.session.commit()

                link = url_for('confirmEmail.confirm_email', token=token, external=True)
                send_link(link, email)
                session['email'] = email # cur_user.email = email
                return redirect(url_for('confirmEmail.confirm_letter'))
        except AttributeError:
            db.session.rollback()
            # flash('Войдите для доступа к закрытым страницам', 'error')
            return redirect(url_for('auth.login'))
    return wrapper