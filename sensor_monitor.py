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


def save_readings(filename, readings):
    try:
        with open(filename, mode="w", newline="", encoding="utf-8") as f:
            writer = csv.writer(f)
            writer.writerow(["sample", "reading"])
            for i in range(len(readings)):
                writer.writerow([i + 1, readings[i]])
        print(f"Data opgeslagen in {filename}")
    except OSError as e:
        print(f"Kon het bestand niet opslaan: {e}")


def load_readings(filename):
    samples = []
    values = []
    try:
        with open(filename, mode="r", newline="", encoding="utf-8") as f:
            reader = csv.DictReader(f)
            for row in reader:
                samples.append(int(row["sample"]))
                values.append(float(row["reading"]))
        return np.array(values)
    except FileNotFoundError:
        print("Bestand niet gevonden.")
        return None
    except (KeyError, ValueError, OSError) as e:
        print(f"Fout bij het inlezen van het CSV-bestand: {e}")
        return None


def plot_readings(readings, threshold, sensor_type):
    x = list(range(1, len(readings) + 1))
    plt.figure()
    plt.plot(x, readings, marker="o", label="Meting")
    plt.axhline(threshold, color="red", linestyle="--", label="Drempelwaarde")
    plt.title(f"{sensor_type} metingen")
    plt.xlabel("Sample nummer")
    plt.ylabel("Waarde")
    plt.grid(True)
    plt.legend()
    plt.savefig("lijngrafiek.png")
    plt.show()


def plot_histogram(readings, sensor_type):
    plt.figure()
    plt.hist(readings, bins=10, edgecolor="black")
    plt.title(f"Verdeling van {sensor_type} metingen")
    plt.xlabel("Waarde")
    plt.ylabel("Aantal")
    plt.grid(True)
    plt.savefig("histogram.png")
    plt.show()


def main():
    print("1 = Nieuwe metingen genereren")
    print("2 = Metingen laden uit CSV")
    keuze = input("Maak een keuze (1 of 2): ").strip()

    if keuze == "2":
        bestandsnaam = input("Naam van CSV-bestand: ").strip()
        readings = load_readings(bestandsnaam)
        if readings is None:
            return
        sensor_type = input("Sensortype voor de grafieken: ").strip() or "sensor"
        while True:
            try:
                threshold = float(input("Alert-drempelwaarde: "))
                break
            except ValueError:
                print("Vul een geldig getal in.")
    else:
        sensor_type, num_readings, min_val, max_val, threshold = get_user_input()
        readings = generate_readings(num_readings, min_val, max_val, seed=42)
        bestandsnaam = input("Bestandsnaam om op te slaan (bijv. metingen.csv): ").strip()
        if bestandsnaam == "":
            bestandsnaam = "metingen.csv"
        save_readings(bestandsnaam, readings)

    stats = calculate_statistics(readings, threshold)
    outliers = find_outliers(readings, threshold)

    print("\n--- Resultaten ---")
    print("Aantal metingen:", stats["aantal"])
    print("Gemiddelde:", round(stats["gemiddelde"], 2))
    print("Minimum:", round(stats["minimum"], 2))
    print("Maximum:", round(stats["maximum"], 2))
    print("Standaardafwijking:", round(stats["std_dev"], 2))
    print("Aantal boven drempel:", stats["boven_drempel"])

    if len(outliers) > 0:
        print("Metingen boven de drempelwaarde:")
        for sample_nr, waarde in outliers:
            print(f"  Sample {sample_nr}: {waarde:.2f}")
    else:
        print("Geen metingen boven de drempelwaarde.")

    plot_readings(readings, threshold, sensor_type)
    plot_histogram(readings, sensor_type)


if __name__ == "__main__":
    main()