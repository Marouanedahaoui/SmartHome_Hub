
import json
from pathlib import Path
from urllib.request import urlopen
from urllib.error import URLError

# Bestandslocatie
MAP = Path(__file__).resolve().parent
WEERBESTAND = MAP / "weerdata.txt"


def weerstation():
    print("\n===== WEERSTATION =====")

    try:
        with open(WEERBESTAND, "r", encoding="utf-8") as bestand:
            regels = bestand.readlines()

        if len(regels) <= 1:
            print("Er zijn geen weergegevens beschikbaar.")
            return

        print("\nDatum | Personen | Binnen | Buiten | Neerslag")
        print("-" * 60)

        for regel in regels[1:]:
            gegevens = regel.split()

            if len(gegevens) != 5:
                print("Ongeldige regel overgeslagen.")
                continue

            try:
                datum = gegevens[0]
                personen = int(gegevens[1])
                binnen = float(gegevens[2])
                buiten = float(gegevens[3])
                neerslag = float(gegevens[4])

                print(
                    f"{datum} | {personen} personen | "
                    f"{binnen:g}°C | {buiten:g}°C | "
                    f"{neerslag:g} mm"
                )

            except ValueError:
                print("Ongeldige weergegevens overgeslagen.")

    except FileNotFoundError:
        print("Het bestand weerdata.txt is niet gevonden.")
        print("Python zoekt hier:", WEERBESTAND)

    except OSError as fout:
        print("Er is een fout bij het lezen:", fout)


def live_weer():
    print("\n===== LIVE WEER UTRECHT =====")

    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=52.09&longitude=5.12"
        "&current=temperature_2m,relative_humidity_2m,"
        "precipitation,wind_speed_10m"
        "&timezone=Europe%2FAmsterdam"
    )

    try:
        with urlopen(url, timeout=10) as response:
            data = json.load(response)

        weer = data["current"]

        temperatuur = weer["temperature_2m"]
        luchtvochtigheid = weer["relative_humidity_2m"]
        neerslag = weer["precipitation"]
        windsnelheid = weer["wind_speed_10m"]

        print("Locatie: Utrecht")
        print(f"Temperatuur: {temperatuur} °C")
        print(f"Luchtvochtigheid: {luchtvochtigheid}%")
        print(f"Neerslag: {neerslag} mm")
        print(f"Windsnelheid: {windsnelheid} km/u")

    except (URLError, TimeoutError):
        print("Geen verbinding met de weer-API.")
        print("Controleer je internetverbinding.")

    except (KeyError, ValueError, OSError) as fout:
        print("De weergegevens konden niet worden opgehaald.")
        print("Foutmelding:", fout)


if __name__ == "__main__":
    weerstation()
