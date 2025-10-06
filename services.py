import json

SERVICES_FILE = "services.json"

def load_services():
    with open(SERVICES_FILE, "r", encoding="utf-8") as f:
        return json.load(f)

def save_services(services_dict):
    with open(SERVICES_FILE, "w", encoding="utf-8") as f:
        json.dump(services_dict, f, ensure_ascii=False, indent=4)
