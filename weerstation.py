import json
from urllib.request import urlopen
from urllib.error import URLError, HTTPError


def Fahrenheit(temp_celcius):
    return 32 + 1.8 * temp_celcius


def gevoelstemperatuur(temp_celcius, windsnelheid, luchtvochtigheid):
    return temp_celcius - (luchtvochtigheid / 100) * windsnelheid


def weerrapport(temp_celcius, windsnelheid, luchtvochtigheid):
    gevoel = gevoelstemperatuur(
        temp_celcius, windsnelheid, luchtvochtigheid
    )

    if gevoel < 0 and windsnelheid > 10:
        return "Het is heel koud en het stormt! Verwarming tot de maxx aan!"

    elif gevoel < 0 and windsnelheid <= 10:
        return "Het is behoorlijk koud! Verwarming aan op de benedenverdieping!"

    elif 0 <= gevoel < 10 and windsnelheid > 12:
        return "Het is best koud en het waait; verwarming aan en roosters dicht onmiddelijk!"

    elif 0 <= gevoel < 10 and windsnelheid <= 12:
        return "Het is koud joh, elektrische kachel op de benedenverdieping aan!"

    elif 10 <= gevoel < 22:
        return "Oeehhhh lekker weer, niet te koudd en niet te warm :)"

    else:
        return "Warm! Doe de f*cking airco aan man"


def vraag_getal(vraag, minimum=None, maximum=None):
    while True:
        invoer = input(vraag).strip()

        if invoer == "":
            return None

        try:
            waarde = float(invoer)

            if not (float("-inf") < waarde < float("inf")):
                print("Voer een geldig getal in.")
                continue

            if minimum is not None and waarde < minimum:
                print(f"De waarde moet minimaal {minimum} zijn.")
                continue

            if maximum is not None and waarde > maximum:
                print(f"De waarde mag maximaal {maximum} zijn.")
                continue

            return waarde

        except ValueError:
            print("Ongeldige invoer. Probeer opnieuw.")


def weerstation():
    totaal_temperatuur = 0

    for dag in range(1, 8):
        temperatuur = vraag_getal(
            f"Wat is op dag {dag} de temperatuur[C]: "
        )

        if temperatuur is None:
            print("bye")
            return

        windsnelheid = vraag_getal(
            f"Wat is op dag {dag} de windsnelheid[m/s]: ",
            minimum=0
        )

        if windsnelheid is None:
            print("bye")
            return

        luchtvochtigheid = vraag_getal(
            f"Wat is op dag {dag} de vochtigheid[%]: ",
            minimum=0,
            maximum=100
        )

        if luchtvochtigheid is None:
            print("bye")
            return

        totaal_temperatuur += temperatuur
        gemiddelde = totaal_temperatuur / dag

        fahrenheit = Fahrenheit(temperatuur)

        print(f"Het is {temperatuur:.1f}C ({fahrenheit:.1f}F)")
        print(weerrapport(temperatuur, windsnelheid, luchtvochtigheid))
        print(f"Gem. temp tot nu toe is {gemiddelde:.1f}")
        print("======================================")

    print("Alle zeven dagen zijn ingevoerd.")


def live_weer():
    url = (
        "https://api.open-meteo.com/v1/forecast"
        "?latitude=52.09&longitude=5.12"
        "&current=temperature_2m,relative_humidity_2m,"
        "precipitation,wind_speed_10m"
    )

    try:
        with urlopen(url, timeout=10) as antwoord:
            gegevens = json.load(antwoord)

        huidig = gegevens["current"]

        print("\nLive weer in Utrecht")
        print("Temperatuur:", huidig["temperature_2m"], "°C")
        print("Luchtvochtigheid:", huidig["relative_humidity_2m"], "%")
        print("Neerslag:", huidig["precipitation"], "mm")
        print("Windsnelheid:", huidig["wind_speed_10m"], "km/u")

    except (URLError, HTTPError, TimeoutError, ValueError, KeyError, OSError):
        print("Het live weer kon niet worden opgehaald.")
