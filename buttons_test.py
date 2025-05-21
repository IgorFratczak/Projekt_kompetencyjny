import RPi.GPIO as GPIO
import time

# Numery pinów GPIO z nazwami i domyślnym stanem
buttons = {
    8: {'name': 'GPIO 14', 'state': GPIO.LOW},
    10: {'name': 'GPIO 15', 'state': GPIO.LOW},
    12: {'name': 'GPIO 18', 'state': GPIO.LOW}
}

# Ustawienie trybu numeracji pinów
GPIO.setmode(GPIO.BCM)

# Konfiguracja pinów jako wejścia z podciąganiem do VCC (pull-up)
for pin in buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Naciśnij przycisk (Ctrl+C aby zakończyć)")

try:
    while True:
        for pin, data in buttons.items():
            if GPIO.input(pin) == GPIO.LOW:  # przycisk wciśnięty
                if data['state'] == GPIO.HIGH:
                    continue  # pomiń, jeśli już wcześniej był wciśnięty
                print(f"{data['name']} został naciśnięty")
                data['state'] = GPIO.HIGH  # aktualizacja stanu
            else:
                data['state'] = GPIO.LOW  # przycisk nie wciśnięty
        time.sleep(0.1)

except KeyboardInterrupt:
    print("\nZakończono działanie")

finally:
    GPIO.cleanup()