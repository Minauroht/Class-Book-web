from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from models import db, reserv
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta

app = Flask(__name__)

basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, "db.sqlite")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///booking.db"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jqiowejrojzxcovnklqnweiorjqwoijroi"
app.config["JSON_AS_ASCII"] = False
engine = create_engine("sqlite:///bookdata.db")
Session = sessionmaker(bind=engine)
session = Session()
db.init_app(app)
db.app = app

bookings = []


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/main")
def homemain():
    return render_template("index.html")


@app.route("/booking", methods=["GET", "POST"])
def booking():
    if request.method == "POST":
        # 양식 데이터 가져오기
        name = request.form["name"]
        # 가져온 체크박스 데이터 문자열에 저장 (변경)
        room = ', '.join(request.form.getlist("room"))
        # 시작 및 종료 시간 추가 (변경)
        start_time = request.form["start-time"]
        end_time = request.form["end-time"]
        time = f"{start_time}-{end_time}"
        group = request.form["group"]
        work = request.form["work"]

        booking = reserv(name=name, room=room, time=time, group=group, work=work)

        db.session.add(booking)
        db.session.commit()
        bookings.append({"name": name, "room": room, "time": time, "group": group, "work": work})
        return redirect(url_for("checking"))
    return render_template("booking.html")


@app.route("/checking", methods=["GET", "POST"])
def checking():
    bookings = reserv.query.order_by(reserv.date.desc()).all()
    return render_template("checking.html", bookings=bookings)


@app.before_first_request
def create_database():
    db.create_all()
    # for data in reserv.query.all():
    #      db.session.delete(data)
    db.session.commit()


def delete_all_data():
    with app.app_context():
        all_data = reserv.query.all()
        for data in all_data:
            db.session.delete(data)
        db.session.commit()
        print("9:30 p.m. base reset")


def start_schedule():
    scheduler = BackgroundScheduler()

    scheduler.add_job(delete_all_data, "cron", hour=21, minute=30)

    scheduler.start()


start_schedule()

if __name__ == "__main__":
    app.run(port=0, host="0.0.0.0", debug=True)
