import json
import os
settings_path = os.path.dirname(os.path.abspath(__file__)) + '/../settings.json'

settings = {
    "display_height": 900,
    "display_width": 1600,
}

def save_settings():
    global settings

    if os.path.isfile(settings_path):
        os.remove(settings_path)

    with open(settings_path, 'w') as file:
        file.write(json.dumps(settings, indent=4))

def settings_read(key: str):
    global settings
    return settings[key]

def settings_write(key: str, val):
    global settings
    settings.update(key, val)
    save_settings()

if not os.path.isfile(settings_path):
    save_settings()
