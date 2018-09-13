from flask import Flask

from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
app = Flask(__name__)
app.secret_key = 'pcos'
app.config['DEBUG'] = 'True'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://klaudiakantor:flights@localhost:5432/flights'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)
class flight(db.Model):
    __tablename__ = 'flight'
    id = db.Column(db.Integer, primary_key=True)
    created_at = db.Column(db.String, default=datetime.now().strftime("%d/%m/%Y"))
    carrier=db.Column(db.String)
    start=db.Column(db.String)
    stop=db.Column(db.String)
    flight_number=db.Column(db.String)
    start_time=db.Column(db.String)
    stop_time=db.Column(db.String)
    price=db.Column(db.String)


    def __init__(self, carrier, start, stop, flight_number, start_time, stop_time, price):
        self.carrier=carrier
        self.start=start
        self.stop=stop
        self.flight_number=flight_number
        self.start_time=start_time
        self.stop_time=stop_time
        self.price=price

    def __repr__(self):
       return '<id {}>'.format(self.id)


