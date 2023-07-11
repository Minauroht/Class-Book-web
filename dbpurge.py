from models import db, reserv, JJH
from app import app

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
    print("DB purge complete")