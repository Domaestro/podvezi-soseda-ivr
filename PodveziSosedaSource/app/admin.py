from flask import redirect, url_for, request, flash
from flask_login import current_user
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .database import db
from .models import Users, Profiles


admin = Admin()


class AdminModelView(ModelView):

    def is_accessible(self):
        # Проверка хотя бы на то, авторизован ли пользователь, потом нужно добавить чтобы пускало только админа
        return current_user.is_authenticated

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))

admin.add_view(AdminModelView(Users, db.session))
admin.add_view(AdminModelView(Profiles, db.session, endpoint="profiles_"))