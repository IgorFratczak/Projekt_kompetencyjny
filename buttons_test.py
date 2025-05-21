import RPi.GPIO as GPIO
import time

# Numery pinów GPIO
buttons = {
    17: "Przycisk 1",
    27: "Przycisk 2",
    22: "Przycisk 3"
}

# Ustawienie trybu numeracji pinów
GPIO.setmode(GPIO.BCM)

# Konfiguracja pinów jako wejścia z podciąganiem do VCC (pull-up)
for pin in buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Naciśnij przycisk (Ctrl+C aby zakończyć)")

try:
    while True:
        for pin, name in buttons.items():
            if GPIO.input(pin) == GPIO.LOW:  # przycisk wciśnięty
                print(f"{name} został naciśnięty")
                time.sleep(0.3)  # opóźnienie, aby uniknąć wielokrotnego wykrycia
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nZakończono działanie")

finally:
    GPIO.cleanup()