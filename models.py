from flask_sqlalchemy import SQLAlchemy
from flask import Flask
import os
from datetime import datetime, timedelta

app = Flask(__name__)
db = SQLAlchemy()

basdir = os.path.abspath(os.path.dirname(__file__))
dbfile = os.path.join(basdir, "booking.db")

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///booking.db"
app.config["SQLALCHEMY_COMMIT_ON_TEARDOWN"] = True
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
app.config["SECRET_KEY"] = "jqiowejrojzxcovnklqnweiorjqwoijroi"

class reserv(db.Model):
    __tablename__ = "reserv"

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(120), nullable=False)
    room = db.Column(db.String(50), nullable=False)
    time = db.Column(db.String(50), nullable=False)
    group = db.Column(db.String(120), nullable=False)
    work = db.Column(db.String(120), nullable=False)
    date = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=9))

class JJH(db.Model):
    __tablename__ = "JJH"

    id = db.Column(db.Integer, primary_key=True)
    jname = db.Column(db.String(120), nullable=False)
    jroom = db.Column(db.String(50), nullable=False)
    jtime = db.Column(db.String(50), nullable=False)
    jgroup = db.Column(db.String(120), nullable=False)
    jwork = db.Column(db.String(120), nullable=False)
    jdate = db.Column(db.DateTime, nullable=False, default=lambda: datetime.utcnow() + timedelta(hours=9))

@app.before_first_request
def create_database():
     db.create_all(app=app)
     db.session.commit()
