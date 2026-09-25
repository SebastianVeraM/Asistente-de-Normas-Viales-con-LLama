import datetime

# Ejemplo simplificado de reglas del programa Hoy No Circula
RULES = {
    "1": ["Monday"],   # Placas terminadas en 1 no circulan lunes
    "2": ["Tuesday"],
    "3": ["Wednesday"],
    "4": ["Thursday"],
    "5": ["Friday"],
    "6": ["Monday"],
    "7": ["Tuesday"],
    "8": ["Wednesday"],
    "9": ["Thursday"],
    "0": ["Friday"]
}

def can_circulate(plate_number, date=None):
    if date is None:
        date = datetime.datetime.now()
    last_digit = plate_number[-1]
    restricted_days = RULES.get(last_digit, [])
    today = date.strftime("%A")
    return today not in restricted_days
