from flask import Flask, jsonify
from sqlalchemy.orm import sessionmaker
from sqlalchemy import create_engine
from db_create import AuthorizedCars, Base
from datetime import datetime

app = Flask(__name__)

engine = create_engine("sqlite:///CarPark.db", echo=True)
Session = sessionmaker(bind=engine)
session = Session()

@app.route("/get_cars", methods=["GET"])
def get_cars():
    cars = session.query(Cars).all()
    cars_list = [
        {
            'carID': car.carID,
            'license_plate': car.license_plate,
            'entry_time': car.entry_time,
            'exit_time': car.exit_time,
            'currently_parked' : car.currently_parked
        }
        for car in cars
    ]
    return jsonify(cars_list)

@app.route("/get_authorized_cars", methods=["GET"])
def get_auth_cars():
    cars = session.query(AuthorizedCars).all()
    cars_list = [
        {
            'acID': car.acID,
            'license_plate': car.license_plate,
            'authorization_start_date': car.authorization_start_date,
            'authorization_end_date': car.authorization_end_date
        }
        for car in cars
    ]
    return jsonify(cars_list)

@app.route('/add_authorization', methods=["POST"])
def insert_auth_car():
    license_plate = request.args.get("license_plate")
    start_time = request.args.get("start_time")
    end_time = request.args.get("end_time")

    try:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')
    except ValueError as e:
        return jsonify({"error": "Invalid date format. Use YYYY-MM-DD HH:MM:SS"}), 400
        
    auth_car = AuthorizedCars(license_plate, start_time, end_time)

    session.add(auth_car)
    session.commit()

    return jsonify({"message": "Car authorization added successfully!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
