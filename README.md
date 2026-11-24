## De vraagstelling laten werken

    import csv
    import random
    import matplotlib.pyplot as plt
    import numpy as np


    def get_user_input():
    sensor_type = input("Sensortype (bijv. temperature of light): ").strip()
    if sensor_type == "":
        sensor_type = "sensor"

    while True:
        try:
            num_readings = int(input("Aantal metingen: "))
            if num_readings <= 0:
                print("Het aantal metingen moet groter zijn dan 0.")
                continue
            break
        except ValueError:
            print("Vul een geldig geheel getal in.")

    while True:
        try:
            min_val = float(input("Minimumwaarde: "))
            max_val = float(input("Maximumwaarde: "))
            if min_val >= max_val:
                print("Minimumwaarde moet kleiner zijn dan de maximumwaarde.")
                continue
            break
        except ValueError:
            print("Vul geldige getallen in voor minimum en maximum.")

    while True:
        try:
            threshold = float(input("Alert-drempelwaarde: "))
            break
        except ValueError:
            print("Vul een geldig getal in voor de drempelwaarde.")

    return sensor_type, num_readings, min_val, max_val, threshold

## Berekeningen

        def generate_readings(num_readings, min_val, max_val, seed=42):
    random.seed(seed)
    data = []
    for _ in range(num_readings):
        waarde = random.uniform(min_val, max_val)
        data.append(waarde)
    return np.array(data)


    def calculate_statistics(readings, threshold):
    aantal = len(readings)
    gemiddelde = np.mean(readings)
    minimum = np.min(readings)
    maximum = np.max(readings)
    std_dev = np.std(readings)
    boven_drempel = int(np.sum(readings > threshold))

    return {
        "aantal": aantal,
        "gemiddelde": gemiddelde,
        "minimum": minimum,
        "maximum": maximum,
        "std_dev": std_dev,
        "boven_drempel": boven_drempel,
    }


    def find_outliers(readings, threshold):
    outliers = []
    for i in range(len(readings)):
        if readings[i] > threshold:
            outliers.append((i + 1, readings[i]))
    return outliers
