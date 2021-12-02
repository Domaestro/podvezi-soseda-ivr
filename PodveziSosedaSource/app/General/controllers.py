from flask import Blueprint, render_template, send_from_directory, make_response
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


# PWA manifest
@general.route('/manifest.json')
def manifest():
    return send_from_directory('static', 'pwa/manifest.json')

# PWA server-workers
@general.route('/sw.js')
def service_worker():
    response = make_response(send_from_directory('static', 'pwa/sw.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response

@general.route('/app.js')
def appjs():
    response = make_response(send_from_directory('static', 'pwa/app.js'))
    response.headers['Cache-Control'] = 'no-cache'
    return response