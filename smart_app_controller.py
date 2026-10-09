
from pathlib import Path

# Bestanden zoeken in dezelfde map als deze Python-code
MAP = Path(__file__).resolve().parent
INPUT_FILE = MAP / "weerdata.txt"
OUTPUT_FILE = MAP / "actuatoren.txt"

print("Python zoekt weerdata hier:", INPUT_FILE)
print("Bestand gevonden:", INPUT_FILE.exists())


def lees_gegevens(inputFile):
    gegevens = []

    with open(inputFile, "r", encoding="utf-8") as bestand:
        regels = bestand.readlines()

    for regel in regels[1:]:
        onderdelen = regel.split()

        if not onderdelen:
            continue

        if len(onderdelen) != 5:
            raise ValueError("Ongeldige regel in weerdata.txt")

        datum = onderdelen[0]
        personen = int(onderdelen[1])
        setpoint = float(onderdelen[2])
        buiten = float(onderdelen[3])
        neerslag = float(onderdelen[4])

        gegevens.append(
            (datum, personen, setpoint, buiten, neerslag)
        )

    return gegevens


def aantal_dagen(inputFile):
    gegevens = lees_gegevens(inputFile)
    return len(gegevens)


def auto_bereken(inputFile, outputFile):
    gegevens = lees_gegevens(inputFile)

    with open(outputFile, "w", encoding="utf-8") as bestand:

        for datum, personen, setpoint, buiten, neerslag in gegevens:

            verschil = setpoint - buiten

            # CV-ketel
            if verschil >= 20:
                cv = 100
            elif verschil >= 10:
                cv = 50
            else:
                cv = 0

            # Ventilatie
            ventilatie = min(personen + 1, 4)

            # Bewatering
            if neerslag < 3:
                bewatering = True
            else:
                bewatering = False

            bestand.write(
                f"{datum};{cv};{ventilatie};{bewatering}\n"
            )

    print("Alle actuatoren zijn berekend!")


def overwrite_settings(outputFile):

    if not outputFile.exists():
        print("Bereken eerst de actuatoren met optie 2.")
        return -1

    datum = input("Voer een datum in (dd-mm-jjjj): ")

    print("\nWelk systeem wil je aanpassen?")
    print("1. CV-ketel")
    print("2. Ventilatie")
    print("3. Bewatering")

    systeem = input("Kies een systeem: ")

    if systeem not in ("1", "2", "3"):
        print("Ongeldig systeem.")
        return -3

    try:
        waarde = int(input("Voer de nieuwe waarde in: "))
    except ValueError:
        print("Je moet een geheel getal invoeren.")
        return -3

    if systeem == "1" and not 0 <= waarde <= 100:
        print("CV moet tussen 0 en 100 liggen.")
        return -3

    if systeem == "2" and not 0 <= waarde <= 4:
        print("Ventilatie moet tussen 0 en 4 liggen.")
        return -3

    if systeem == "3" and waarde not in (0, 1):
        print("Bewatering moet 0 of 1 zijn.")
        return -3

    with open(outputFile, "r", encoding="utf-8") as bestand:
        regels = bestand.readlines()

    nieuwe_regels = []
    gevonden = False

    for regel in regels:
        onderdelen = regel.strip().split(";")

        if len(onderdelen) != 4:
            nieuwe_regels.append(regel)
            continue

        if onderdelen[0] == datum:
            gevonden = True

            if systeem == "1":
                onderdelen[1] = str(waarde)

            elif systeem == "2":
                onderdelen[2] = str(waarde)

            elif systeem == "3":
                onderdelen[3] = str(bool(waarde))

            regel = ";".join(onderdelen) + "\n"

        nieuwe_regels.append(regel)

    if not gevonden:
        print("Datum niet gevonden.")
        return -1

    with open(outputFile, "w", encoding="utf-8") as bestand:
        bestand.writelines(nieuwe_regels)

    print("De waarde is succesvol aangepast!")
    return 0


def smart_app_controller():

    while True:

        print("\n===== SMART APP CONTROLLER =====")
        print("1. Aantal dagen weergeven")
        print("2. Actuatoren automatisch berekenen")
        print("3. Berekende waarde overschrijven")
        print("4. Terug naar hoofdmenu")

        keuze = input("Maak een keuze (1-4): ")

        try:
            if keuze == "1":
                dagen = aantal_dagen(INPUT_FILE)
                print("Aantal dagen:", dagen)

            elif keuze == "2":
                auto_bereken(INPUT_FILE, OUTPUT_FILE)

            elif keuze == "3":
                overwrite_settings(OUTPUT_FILE)

            elif keuze == "4":
                print("Terug naar het hoofdmenu...")
                break

            else:
                print("Ongeldige keuze. Probeer opnieuw.")

        except FileNotFoundError:
            print("FOUT: Het benodigde tekstbestand bestaat niet.")
            print("Gezocht op:", INPUT_FILE)
            print("Controleer of weerdata.txt in dezelfde map staat.")

        except ValueError as fout:
            print("Ongeldige gegevens:", fout)

        except OSError as fout:
            print("Bestandsfout:", fout)


if __name__ == "__main__":
    smart_app_controller()
