from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView

from .database import db
from .models import Users, Profiles


admin = Admin()

admin.add_view(ModelView(Users, db.session))
admin.add_view(ModelView(Profiles, db.session, endpoint="profiles_"))