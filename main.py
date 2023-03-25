import urllib

from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from faker import Faker
from flask_swagger import swagger
import random

# ODBC sürücüsü kullanarak bağlantı dizesini oluşturuluyor.
params = urllib.parse.quote_plus("Driver={ODBC Driver 18 for SQL Server};Server=tcp:airlinedatabaseserver.database.windows.net,1433;Database=FlightDB;Uid=sqladmin;Pwd={Password123};Encrypt=yes;TrustServerCertificate=no;Connection Timeout=30;")

app = Flask(__name__)
app.config['SECRET_KEY'] = 'supersecret'
app.config['SQLALCHEMY_DATABASE_URI'] = "mssql+pyodbc:///?odbc_connect=%s" % params
app.config['SQLALCHEMY_COMMIT_ON_TEARDOWN'] = True
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


@app.route('/swagger')
def get_docs():
    return render_template('swaggerui.html')


class Flight(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    date = db.Column(db.String(10), nullable=False)
    flight_no = db.Column(db.String(10), nullable=False)
    departure = db.Column(db.String(50), nullable=False)
    arrival = db.Column(db.String(50), nullable=False)
    seats = db.Column(db.Integer, nullable=False)


@app.route('/flights', methods=['GET'])
def query_flights():
    date = request.args.get('date', '')
    departure = request.args.get('departure', '')
    arrival = request.args.get('arrival', '')
    num_passengers = int(request.args.get('num_passengers', 1))

    flights = Flight.query.filter_by(date=date, departure=departure, arrival=arrival)
    results = []

    for flight in flights:
        if flight.seats >= num_passengers:
            results.append({
                'date': flight.date,
                'departure': flight.departure,
                'arrival': flight.arrival,
                'seats': flight.seats,
                'flight_no': flight.flight_no,
            })

    return jsonify({'flights': results})


@app.route('/buy', methods=['POST'])
def buy_ticket():
    auth = request.authorization

    if not auth:
        return jsonify({'message': 'Authorization Required'}), 401

    username = auth.username
    password = auth.password

    if username != 'airline' or password != 'password':
        return jsonify({'message': 'Invalid Username or Password'}), 401

    date = request.args.get('date', '')
    departure = request.args.get('departure', '')
    arrival = request.args.get('arrival', '')

    flight = Flight.query.filter_by(date=date, departure=departure, arrival=arrival).first()

    if not flight:
        return jsonify({'message': 'No Flight Found'}), 404

    if flight.seats == 0:
        return jsonify({'message': 'Flight is Full'}), 400

    flight.seats -= 1
    db.session.commit()

    return jsonify({'message': f'Ticket Booked for  Flight {flight.flight_no}'})


def fill_flight_database(num_records):
    faker = Faker()

    for i in range(num_records):
        countries = ["Adana", "Ankara", "Alanya", "Antalya", "Balıkesir", "Bursa", "İstanbul", "Gaziantep", "İzmir",
                     "Tekirdağ", "Sinop", "Samsun", "Muğla"]
        departure_city = random.choice(countries)
        countries.remove(departure_city)
        arrival_city = random.choice(countries)

        flight = Flight(
            date=faker.date_between(start_date='-30d', end_date='+30d').strftime('%Y-%m-%d'),
            flight_no=faker.random_int(min=100, max=999),
            departure=departure_city,
            arrival=arrival_city,
            seats=random.randint(1, 50)
        )

        db.session.add(flight)

    db.session.commit()

# İlk kez oluşturma ve tabloyu random değerlerle doldurmak için kullanıldı.
# db.create_all()
# fill_flight_database(450)

# for flight in Flight.query.all():
#     print(f"{flight.id}|{flight.date}|{flight.flight_no}|{flight.departure}|{flight.arrival}|{flight.seats}")

# print(len(Flight.query.all()))


if __name__ == '__main__':
    app.run(debug=True)
