import pickle
import RPi.GPIO as GPIO
from main2 import gate_open
import time
import json


class GPIO_Handler:
    def __init__(self):
        GPIO.setmode(GPIO.BCM)
        GPIO.setwarnings(False)
        self.output_pins = [21, 20, 16]
        self.input_pins = [1, 7, 8]
        for pin in self.output_pins:
            GPIO.setup(pin, GPIO.OUT)
        for pin in self.input_pins:
            GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_DOWN)

    def read_gpio(self):
        try:
            with open("database/gpio_data.pickle", "rb") as f:
                gpio_data = pickle.load(f)
            return gpio_data
        except FileNotFoundError:
            return None
        except Exception as e:
            return None

    def handle_gpio_recognition(self):
        global gate_open
        gpio = self.read_gpio()
        print(gpio.get("outputs", []))
        if gpio is not None:
            outputs = gpio.get("outputs", [])
            for index, action in enumerate(outputs):
                if action == "recognition: high for 10 seconds":
                    if index < len(self.output_pins):
                        pin = self.output_pins[index]
                        print(f"Opening gate on {pin}, action {action}")
                        GPIO.output(pin, GPIO.HIGH)
                        gate_open = True
                        with open("database/global_data.json", 'r') as f:
                            global_vars = json.load(f)

                        global_vars["gate_state"] = gate_open

                        with open("database/global_data.json", 'w') as f:
                            json.dump(global_vars, f, indent=4)
                        time.sleep(10)
                        GPIO.output(pin, GPIO.LOW) 
                        gate_open = False
                        with open("database/global_data.json", 'r') as f:
                            global_vars = json.load(f)

                        global_vars["gate_state"] = gate_open

                        with open("database/global_data.json", 'w') as f:
                            json.dump(global_vars, f, indent=4)

                if action == "recognition: impulse" or action == "car passed input: impulse":
                    print("Pracuje")
                    if index < len(self.output_pins):
                        pin = self.output_pins[index]
                        print(f"Opening gate on {pin}, action {action}")
                        GPIO.output(pin, GPIO.HIGH)
                        gate_open = True
                        time.sleep(1)
                        GPIO.output(pin, GPIO.LOW)

    def handle_gpio_inputs(self):
        for pin in self.input_pins:
            if GPIO.input(pin) == GPIO.HIGH:
                gpio = self.read_gpio()
                if gpio is not None:
                    outputs = gpio.get("outputs", [])
                    for index, action in enumerate(outputs):
                        if action == "car passed input: impulse" or "recog & car passed input: impulse":
                            if index < len(self.output_pins):
                                output_pin = self.output_pins[index]
                                GPIO.output(pin, GPIO.HIGH)
                                gate_open = True
                                time.sleep(1)
                                GPIO.output(pin, GPIO.LOW)

if __name__ == '__main__':
    handle_gpio()