from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
from models import db, reserv
from flask_sqlalchemy import SQLAlchemy
import sqlite3
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

app = Flask(__name__)

# 현재있는 파일의 디렉토리 절대경로
basdir = os.path.abspath(os.path.dirname(__file__))
# basdir 경로안에 DB파일 만들기
dbfile = os.path.join(basdir, 'db.sqlite')

# SQLAlchemy 설정

# 내가 사용 할 DB URI
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///booking.db'
# 비지니스 로직이 끝날때 Commit 실행(DB반영)
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
# 수정사항에 대한 TRACK
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# SECRET_KEY
app.config['SECRET_KEY'] = 'jqiowejrojzxcovnklqnweiorjqwoijroi'
app.config['JSON_AS_ASCII'] = False
engine = create_engine('sqlite:///bookdata.db')
Session = sessionmaker(bind=engine)
session = Session()
db.init_app(app)
db.app = app

bookings=[]
@app.route('/')
def home():
    return render_template('index.html')


@app.route('/booking', methods=['GET', 'POST'])
def booking():
    if request.method == 'POST':
        # 양식 데이터 가져오기
        name = request.form['name']
        room = request.form['room']
        time = request.form['time']
        group = request.form['group']
        work = request.form['work']

        booking = reserv(name=name, room=room, time=time, group=group, work=work)

        db.session.add(booking)
        db.session.commit()
        # 리뷰를 목록에 추가
        bookings.append({'name': name, 'room': room, 'time': time, 'group': group, 'work': work})
        # 리뷰 목록 페이지로 리디렉션
        return redirect(url_for('checking'))
    # 요청 방법이 GET인 경우 검토 양식 렌더링
    return render_template('booking.html')


@app.route('/checking', methods=['GET', 'POST'])
def checking():
    # 데이터베이스에서 모든 리뷰 검색
    bookings = reserv.query.all()
    # 리뷰 데이터로 리뷰 목록 템플릿 렌더링
    return render_template('checking.html', bookings=bookings)

@app.before_first_request
def create_database():
    #db.session.query(reserv).delete() #<--이거 켜면 데이터 다 날아감. 주석 취소할 때 주의할 것.
    db.create_all()
    db.session.commit()


if __name__ == "__main__":
    app.run(port=0, host='0.0.0.0', debug=True)
