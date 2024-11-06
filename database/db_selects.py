from sqlalchemy.orm import sessionmaker
from database.db_create import engine, AuthorizedCars, Cars
#from db_create import AuthorizedCars, Cars

class Selects():
    def __init__(self):
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def check_car_exist(self, license_plate):
        car_exists = self.session.query(Cars).filter_by(license_plate=license_plate).first()
        if car_exists:
            return True
        else:
            return False

    def check_authorization(self, license_plate):
        check_auth = self.session.query(AuthorizedCars).filter_by(license_plate=license_plate).first()
        if check_auth:
            return True
        else:
            return False

if __name__ == "__main__":
    selects = Selects()
    print(selects.check_authorization('EE12345'))