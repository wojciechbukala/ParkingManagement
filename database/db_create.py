import os
from sqlalchemy import create_engine, ForeignKey, Column, String, Integer, DateTime, Float, Boolean
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from datetime import datetime

db_path = os.path.join(os.path.dirname(__file__), "CarPark.db")
engine = create_engine(f"sqlite:///{db_path}", echo=True)
Base = declarative_base()

class AuthorizedCars(Base):
    __tablename__ = "AuthorizedCars"

    acID = Column("lpID", Integer, primary_key=True)
    license_plate = Column("license_plate", String)
    authorization_start_date = Column("authorization_start_date", DateTime)
    authorization_end_date = Column("authorization_end_date",DateTime)

    def __init__(self, license_plate, authorization_start_date, authorization_end_date):
        self.license_plate = license_plate
        self.authorization_start_date = authorization_start_date
        self.authorization_end_date = authorization_end_date

    def __repr__(self):
        return f"({self.lpID}, {self.license_plate}, {self.authorization_start_date}, {self.authorization_end_date})"

class Cars(Base):
    __tablename__ = "Cars"

    carID = Column("carID", Integer, primary_key=True)
    license_plate = Column("license_plate", String)
    entry_time = Column("entry_time", DateTime)
    exit_time = Column("exit_time", DateTime)
    currently_parked = Column("currently_parked", Boolean)

    def __init__(self, license_plate, entry_time = None):
        self.license_plate = license_plate
        self.entry_time = entry_time if entry_time else datetime.now()

    def __repr__(self):
        return f"({self.carID}, {self.license_plate}, {self.entry_time}, {self.exit_time}, {self.currently_parked})"

class Payments(Base):
    __tablename__ = "Payments"

    paymentID = Column("paymentID", Integer, primary_key=True)
    carID = Column(Integer, ForeignKey("Cars.carID"))
    amount = Column("amout", Float)
    payment_date = Column("payment_date", DateTime)

    def __init__(self, carID, amount, payment_date):
        self.carID = carID
        self.amount = amount
        self.payment_date = payment_date

    def __repr__(self):
        return f"({self.paymentID}, {self.carID}, {self.amount}, {self.payment_date})"



Base.metadata.create_all(bind=engine)

Session = sessionmaker(bind=engine)
session = Session()
