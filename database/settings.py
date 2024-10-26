#"mode": 0, // 0 - Anyone, 1 - Authorized
#"payment_mode": 0 - Free, 1 - Entrance fee, 2 - Fee per hour
#"region": 0 // 0 - EU, 1 - NA, 2 - ASIA

import json

settings = {}

def load_settings():
    global settings
    with open('database/settings.json', 'r') as file:
        settings = json.load(file)

def save_settings():
    global settings
    with open('settings.json', 'w') as file:
        json.dump(settings, file, indent=4)

if __name__ == '__main__':
    load_settings()