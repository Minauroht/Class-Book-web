from models import db, reserv, JJH
from app import app

def purgeDB():
    db.create_all()
    reserv_data = reserv.query.all()
    jjh_data = JJH.query.all()

    for data in reserv_data:
        db.session.delete(data)

    for data in jjh_data:
        db.session.delete(data)

    db.session.commit()

    print("DB purge complete")

if __name__ == "__main__":
    with app.app_context():
        purgeDB()