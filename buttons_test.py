import RPi.GPIO as GPIO
import time

# Numery pinów GPIO z nazwami i domyślnym stanem
buttons = {
    14: {'name': 'GPIO 14', 'state': GPIO.LOW},
    15: {'name': 'GPIO 15', 'state': GPIO.LOW},
    18: {'name': 'GPIO 18', 'state': GPIO.LOW}
}

# Ustawienie trybu numeracji pinów
GPIO.setmode(GPIO.BCM)

# Konfiguracja pinów jako wejścia z podciąganiem do VCC (pull-up)
for pin in buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

print("Stan przycisków (Ctrl+C aby zakończyć):")

try:
    while True:
        for pin, data in buttons.items():
            state = GPIO.input(pin)
            data['state'] = state
            print(f"{data['name']}: {0 if state == GPIO.LOW else 1}")
        print("-" * 30)
        time.sleep(0.5)

except KeyboardInterrupt:
    print("\nZakończono działanie")

finally:
    GPIO.cleanup()