from smart_app_controller import smart_app_controller
from weerstation import weerstation, live_weer


def main():
    while True:
        print("\n===== SMARTHOME HUB =====")
        print("1. Smart App Controller")
        print("2. Weerstation")
        print("3. Live weer Utrecht")
        print("4. Stoppen")

        keuze = input("Maak een keuze (1-4): ")

        if keuze == "1":
            smart_app_controller()

        elif keuze == "2":
            weerstation()

        elif keuze == "3":
            live_weer()

        elif keuze == "4":
            print("Bedankt voor het gebruiken van SmartHome Hub!")
            break

        else:
            print("Ongeldige keuze. Probeer opnieuw.")


if __name__ == "__main__":
    main()