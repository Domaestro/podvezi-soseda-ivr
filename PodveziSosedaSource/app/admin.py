from flask import redirect, url_for, request, flash
from flask_login import current_user
from flask_admin import Admin, AdminIndexView
from flask_admin.contrib.sqla import ModelView

from config import Config
from .database import db
from .models import Users, Profiles, Trips, Email_Confirm_Tokens


class AdminModelView(ModelView):
    column_display_pk = True
    def is_accessible(self):
        user = Users.query.filter(Users.id == current_user.get_id()).first()
        return user.email==Config.admin_login

    def inaccessible_callback(self, name, **kwargs):
        return redirect(url_for('auth.login', next=request.url))


class AdminIndex(AdminIndexView):
    def is_accessible(self):
        user = Users.query.filter(Users.id == current_user.get_id()).first()
        return user.email==Config.admin_login


admin = Admin(index_view=AdminIndex())

admin.add_view(AdminModelView(Users, db.session))
admin.add_view(AdminModelView(Profiles, db.session, endpoint="profiles_"))
admin.add_view(AdminModelView(Trips, db.session))
admin.add_view(AdminModelView(Email_Confirm_Tokens, db.session))