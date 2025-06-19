def calcular(actividad: str, cantidad: float) -> float:
    factores = {
        "car": 0.2,                 #por km
        "plane": 150,               #hora de vuelo
        "burger": 2.5,              #por hamburguesa
        "electricity": 0.4,         #por kWh
        "train": 0.05,              #por km
        "shower": 0.3,              #por cada 10 min
        "washing_machine": 0.6,     # por ciclo de lavado (agua caliente)
        "dryer": 2.4,               # por ciclo de secadora
        "light": 0.04,              # por hora encendida
        "computer": 0.06,           # por hora de uso
        "heating": 2.0,             # por hora de calefacción media (gas natural)
        "motorcycle": 0.1,          # por km
        "coffee": 0.2,              # por taza
        "bottle_water": 0.15,       # por botella de 500 ml
        "chicken": 6.0,             # por kg
        "beef": 27.0,               # por kg
        "cheese": 13.5,             # por kg
        "tv": 0.1,                  # por hora
        "fridge": 1.5,              # por día
        "wifi": 0.05,        # por día
    }

    actividad = actividad.lower()
    if actividad not in factores:
        raise ValueError("Unrecognized activity")

    return factores[actividad] * cantidad