from flask import Flask, jsonify, request, send_file
from sqlalchemy.orm import sessionmaker
from db_create import engine, Cars, AuthorizedCars, Base
from datetime import datetime
import settings as st
import os
import json

app = Flask(__name__)

Session = sessionmaker(bind=engine)
session = Session()

st.load_settings()

@app.route("/status", methods=["GET"])
def status():
    return jsonify({"status": "Server is running"}), 200

@app.route("/send_detection_img", methods=["GET"])
def send_detection_img():
    if not os.path.exists("detected.png"):
        return jsonify({"error": "File not found"}), 404
    
    try:
        return send_file("detected.png", mimetype='image/png')
    except Exception as e:
        return str(e), 500

@app.route("/send_detection_data", methods=["GET"])
def send_detection_data():
    with open("detection_data.json", 'r') as f:
        detected_data = json.load(f)
        return jsonify(detected_data), 200
    

@app.route("/change_settings", methods=["POST"])
def change_settings():
    new_settings = request.get_json()
    client_ip = request.remote_addr

    if new_settings is None:
        return jsonify({"error": "No settings"}), 400

    new_settings["client_ip"] = client_ip

    for setting_name, setting_val in new_settings.items():
        if setting_val is not None:
            st.settings[setting_name] = setting_val

    st.save_settings()
    return jsonify({"message": "Settings updated successfully"}), 200

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
    data = request.get_json()

    license_plate = data.get("license_plate")
    start_time_str = data.get("start_date")
    end_time_str = data.get("end_date")

    try:
        start_time = datetime.strptime(start_time_str, '%Y-%m-%d %H:%M:%S')
        end_time = datetime.strptime(end_time_str, '%Y-%m-%d %H:%M:%S')

        auth_car = AuthorizedCars(license_plate=license_plate, authorization_start_date=start_time, authorization_end_date=end_time)

        session.add(auth_car)
        session.commit()

        return jsonify({"message": "Car authorization added successfully!"}), 201
    except Exception as e:
        session.rollback()
        return jsonify({"error": f"Failed to add authorization: {str(e)}"}), 500

@app.route('/delete_car', methods=['POST'])
def delete_car():
    data = request.get_json()

    license_plate = data.get("license_plate")

    car_to_remove = session.query(Cars).filter_by(license_plate=license_plate).first()
    if car_to_remove:
        session.delete(car_to_remove)
        session.commit()
        return jsonify({"message": "Car authorization removed successfully!"}), 201

    return jsonify({"message": "Can not find the car!"}), 201

@app.route('/delete_authorization', methods=['POST'])
def delete_auth_car():
    data = request.get_json()

    license_plate = data.get("license_plate")

    car_to_remove = session.query(AuthorizedCars).filter_by(license_plate=license_plate).first()
    if car_to_remove:
        session.delete(car_to_remove)
        session.commit()
        return jsonify({"message": "Car authorization removed successfully!"}), 201

    return jsonify({"message": "Can not find the car!"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
