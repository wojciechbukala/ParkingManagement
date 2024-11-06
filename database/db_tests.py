from db_selects import Selects
from db_inserts import Inserts

class DatabaseTests:
    def __init__(self):
        self.init_communication()

    def init_communication(self):
        self.selects = Selects()
        self.inserts = Inserts()

    def insert_car(self, license_plate):
        self.inserts.insert_car(license_plate)

if __name__ == "__main__":
    db_test = DatabaseTests()
    db_test.insert_car("TEST2")
