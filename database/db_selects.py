from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from database.db_create import AuthorizedCars, Cars

class Selects():
    def __init__(self):
        engine = create_engine("sqlite:///CarPark.db", echo=True)
        Session = sessionmaker(bind=engine)
        self.session = Session()

    def __del__(self):
        self.session.close()

    def check_authorization(self, license_plate):
        check_auth = self.session.query(AuthorizedCars).filter_by(license_plate=license_plate).first()
        if check_auth:
            return True
        else:
            return False

if __name__ == "__main__":
    selects = Selects()
    print(selects.check_authorization('EE12345'))