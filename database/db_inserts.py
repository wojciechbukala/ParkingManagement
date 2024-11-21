from sqlalchemy.orm import sessionmaker
from database.db_create import engine, AuthorizedCars, Cars
#from db_create import AuthorizedCars, Cars
from datetime import datetime


class Inserts():
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def insert_car(self, license_plate):
        car = Cars(license_plate)
        car.currently_parked = True
        self.session.add(car)
        print("Auto dodane!")
        self.session.commit()

    def car_exit(self, lp):
        exiting_car = self.session.query(Cars).filter_by(license_plate=lp, currently_parked=True).first()
        if exiting_car:
            exiting_car.exit_time = datetime.now()
            exiting_car.currently_parked = False
            self.session.commit()


    def remove_expider_authorization(self):
        expired_cars = self.session.query(AuthorizedCars).filter_by(authorization_end_date < now)

        for expired_car in expired_cars:
            self.session.delete(expired_car)

        self.session.commit()

    def insert_auth_car(self, license_plate, start_time, end_time):
        auth_car = AuthorizedCars(license_plate, start_time, end_time)
        self.session.add(auth_car)
        self.session.commit()

    def check_if_auth_valid(self, start_time):
        if start_time < datetime.now():
            return False
        return True
    
    def remove_auth_car(self, license_plate): 
        car_to_remove = self.session.query(AuthorizedCars).filter_by(license_plate=license_plate).first()
        if car_to_remove:
            self.session.delete(car_to_remove)
            self.session.commit()

if __name__ == "__main__":
    insert = Inserts()
    # insert.insert_car("ZS1235", datetime(2024, 10, 9, 8, 0, 0),
    #                         datetime(2024, 12, 31, 23, 59, 59))
    insert.insert_car("DW1235")
    insert.insert_car("WE1235")
    insert.insert_car("PO1235")