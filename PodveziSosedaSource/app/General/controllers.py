from flask import Blueprint, render_template
from flask_login import login_required

from app.utils.utils import confirm_required


general = Blueprint('general', __name__)


@general.route("/index", methods=("POST", "GET"))
@general.route("/", methods=("POST", "GET"))
@confirm_required
@login_required
def index():
    return render_template("index.html")


# Страница 404
@general.app_errorhandler(404)
def page_not_found(e):
    return render_template('Errors/404.html'), 404