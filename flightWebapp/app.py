from flask import Flask, render_template, request, session
from flask_sqlalchemy import SQLAlchemy
import pandas as pd
import os
from dotenv import load_dotenv

env_path = os.path.join(os.getcwd(), '.env')
load_dotenv(dotenv_path=env_path)
DATABASE_PASSWORD = os.getenv("DATABASE_PASSWORD")
DATABASE_USER = os.getenv("DATABASE_USER")

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://' + DATABASE_USER + ':' + DATABASE_PASSWORD + '@localhost:5432/flights'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = 'True'
db = SQLAlchemy(app)
from models import Flights


@app.route('/')
def index():
    return render_template('index.html')


@app.route("/form")
def show_form():
    return render_template('form.html')


@app.route('/result', methods=['POST'])
def search():
    # Get data from FORM
    form_date = request.form['date']
    form_start = request.form['start']
    form_stop = request.form['stop']
    flights_list = db.session.query(Flights.created_at, Flights.date, Flights.start, Flights.stop, Flights.start_time,
                                    Flights.stop_time, Flights.price, Flights.carrier).filter(Flights.date == form_date,
                                                                                              Flights.start.like(
                                                                                                  form_start + '%'),
                                                                                              Flights.stop.like(
                                                                                                  form_stop + '%')).all()
    flights_set=set(flights_list)
    created_at = []
    price = []
    carrier = []
    for row in flights_set:
        created_at.append(row[0])
        price.append(float(row[6]))
        carrier.append(row[7])
    df = pd.DataFrame({'time': created_at, 'price': price, 'carrier': carrier})
    df_wizzair = df[df['carrier'] == 'wizzair']
    df_ryanair = df[df['carrier'] == 'ryanair']
    df_result = pd.merge(df_wizzair, df_ryanair, on='time').drop(['carrier_x', 'carrier_y'], axis=1)
    df_result.columns = ['time', 'wizzair', 'ryanair']
    chart_data = df_result.values.tolist()
    return render_template('result.html', data=flights_set, chart_data=chart_data)


if __name__ == '__main__':
    app.run()
