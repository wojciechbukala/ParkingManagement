import pickle

def read_gpio():
    try:
        with open("database/gpio_data.pickle", "rb") as f:
            gpio_data = pickle.load(f)
        return gpio_data
    except FileNotFoundError:
        return None
    except Exception as e:
        return None

# Wywołanie funkcji
read_gpio_data()