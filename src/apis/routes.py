from flask import Blueprint, request, Response, flash
from flask_restful import Api, Resource
from flask_cors import CORS
from src.models.db import db_session as session
from src.models.base import Base
from flask import session as api_session
from src.models.series import Series, SeriesSchema
from src.models.users import Users, UsersSchema
from src.models.tournaments import Tournaments, TournamentsSchema
from src.utils.exceptions import HTTPError
from src.utils.validate import data_validation
from src.utils.logger import logger
from src.utils.auth import login_required, authenticate_user
from flask import Flask, render_template, url_for, redirect
from src.config import Configurations as Config


config = Config()

app_v1 = Blueprint('api_v1', __name__)
app = Flask(__name__)
app.secret_key = config.SECRET_KEY
app.register_blueprint(app_v1)
CORS(app_v1)


@app.route('/register', methods=["GET", "POST"])
def register():
    logger.error("{} {}".format("is_valid_user", request.method))

    if request.method == "POST":
        form_data = request.form
        data_validation(form_data, ["username", "password", "email"])
        user_schema = UsersSchema()
        user_obj, error = user_schema.load({
            "username": form_data.get('username'),
            "password": form_data.get('password'),
            "email": form_data.get('email')
        })
        if error:
            logger.error("Failed to process request.", extras={
                "username": form_data.get('username')})
            raise HTTPError(400, error)
        try:
            session.add(user_obj)
            session.commit()
            return redirect(url_for("login"))
        except Exception as exc:
            session.rollback()
            logger.error("Failed to process request {}".format(str(exc)))
            raise HTTPError(500, {"error": str(exc)})
    else:
        return render_template("register.html")


@app.route('/login', methods=["GET", "POST"])
def login():
    if request.method == "POST":
        try:
            form_data = request.form
            data_validation(form_data, ['username', 'password'])
            is_valid_user = authenticate_user(form_data.get('username'),
                                              form_data.get('password'))
            if not is_valid_user:
                raise HTTPError(401)
            api_session['token'] = is_valid_user.get('user_secret')
            return redirect(url_for('index'))
        except Exception as exc:
            logger.error(str(exc))
            return render_template('login.html')
    else:
        return render_template('login.html')


@app.route('/logout')
def logout():
    api_session.clear()
    return redirect(url_for('login'))


@app.route('/tournament', methods=["GET"])
def tournament():
    tournaments_schema = TournamentsSchema()
    date_start = request.args.get("date_start")
    date_end = request.args.get("date_end")
    series_name = request.args.get("series_name")
    if series_name:
        response = tournaments_schema.filter_by_series(session, series_name)
    elif date_start and date_end:
        response = tournaments_schema.filter_by_date_range(session, date_start, date_end)
    else:
        response = tournaments_schema.all(session)
    return render_template('tournament.html', items=response)


@app.route('/create_tournament', methods=["GET", "POST"])
def create_tournament():
    tournament_schema = TournamentsSchema()
    series_schema = SeriesSchema()
    series_names = series_schema.all(session)
    if request.method == "POST":
        form_data = request.form
        data_validation(form_data, [
            'series_id', 'name', 'date_start', 'date_end', 'city', 'country'])
        tournaments_obj, error = tournament_schema.load(dict(
            series_id=form_data.get("series_id"),
            name=form_data.get("name"),
            city=form_data.get("city"),
            country=form_data.get("country"),
            date_start=form_data.get("date_start"),
            date_end=form_data.get("date_end")
        ))
        try:
            session.add(tournaments_obj)
            session.commit()
        except Exception as exc:
            session.rollback()
            raise HTTPError(500, {"error": str(exc)})
        return redirect(url_for("create_tournament"))
    return render_template('create_tournament.html', series_names=series_names)


@app.route('/create_series', methods=["GET", "POST"])
def create_series():
    series_schema = SeriesSchema()
    if request.method == "POST":
        form_data = request.form
        data_validation(form_data, ['name', 'date_start', 'date_end'])
        series_obj, error = series_schema.load(
            dict(name=form_data.get("name"),
                 date_start=form_data.get("date_start"),
                 date_end=form_data.get("date_end")
                 )
        )
        try:
            session.add(series_obj)
            session.commit()
        except Exception as exc:
            session.rollback()
            logger.error("Failed to process request {}".format(str(exc)))
            raise HTTPError(500, {"error": str(exc)})
        return redirect(url_for("create_series"))
        flash("Series successfully created")
    return render_template('create_series.html')


@app.route('/')
def index():
    if api_session.get('token'):
        return render_template('index.html')
    else:
        return redirect(url_for('login'))
