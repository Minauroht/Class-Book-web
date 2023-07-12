from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from models import db, reserv, JJH
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from apscheduler.schedulers.background import BackgroundScheduler
from datetime import datetime, timedelta
#야범준 왔다감
#정민우 왔다감
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
jbookings = []

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

@app.route("/JJHbooking", methods=["GET", "POST"]) #자주학 예약 페이지용 템플릿
def JJHbooking():
    if request.method == "POST":
        # 양식 데이터 가져오기
        jname = request.form["jname"]
        # 가져온 체크박스 데이터 문자열에 저장 (변경)
        jroom = ', '.join(request.form.getlist("jroom"))
        # 시작 및 종료 시간 추가 (변경)
        jstart_time = request.form["jstart-time"]
        jend_time = request.form["jend-time"]
        jtime = f"{jstart_time}-{jend_time}"
        jgroup = request.form["jgroup"]
        jwork = request.form["jwork"]

        jbooking = JJH(jname=jname, jroom=jroom, jtime=jtime, jgroup=jgroup, jwork=jwork)

        db.session.add(jbooking)
        db.session.commit()
        jbookings.append({"jname": jname, "jroom": jroom, "jtime": jtime, "jgroup": jgroup, "jwork": jwork})
        return redirect(url_for("JaJuHak"))
    return render_template("JJHbooking.html")

@app.route("/checking", methods=["GET", "POST"])
def checking():
    bookings = reserv.query.order_by(reserv.date.desc()).all()
    return render_template("checking.html", bookings=bookings)

@app.route("/JaJuHak", methods=["GET", "POST"])
def JaJuHak():
    jbookings = JJH.query.order_by(JJH.jdate.desc()).all()
    return render_template("JaJuHak.html", jbookings=jbookings)

# dlrj
def number():
    numbers = range(1, 5)  # 1부터 4까지의 숫자 범위 생성
    return render_template('checking.html', numbers=numbers)


@app.before_first_request
def purgeDB():
    db.create_all()
    reserv_data = reserv.query.all()
    jjh_data = JJH.query.all()
        
    for data in reserv_data:
        db.session.delete(data)
       
    for data in jjh_data:
        db.session.delete(data)
        
    db.session.commit()

'''
def delete_all_data():
    with app.app_context():
        all_data = reserv.query.all(), JJH.query.all()
        for data in all_data:
            db.session.delete(data)
        db.session.commit()
        print("9:30 p.m. base reset")


def start_schedule():
    scheduler = BackgroundScheduler()

    scheduler.add_job(delete_all_data, "cron", hour=21, minute=30)

    scheduler.start()


start_schedule()
'''

if __name__ == "__main__":
    app.run(port=0, host="0.0.0.0", debug=True)


