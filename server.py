from flask import Flask, render_template, request
from flask import jsonify
import threading
from data_analysis_utils import generate_report

try:
    import RPi.GPIO as GPIO
except (ImportError, RuntimeError):
    class MockGPIO:
        BCM = 'BCM'
        OUT = 'OUT'
        IN = 'IN'
        LOW = 0
        HIGH = 1
        PUD_UP = 'PUD_UP'

        def setmode(self, *args, **kwargs): pass
        def setup(self, *args, **kwargs): pass
        def output(self, *args, **kwargs): pass
        def input(self, *args, **kwargs): return self.HIGH
        def setwarnings(self, *args, **kwargs): pass
    GPIO = MockGPIO()
import time
import socket
import multiprocessing
from multiprocessing import Value

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
import os

# Ścieżka do pliku kalibracyjnego
CALIBRATION_FILE = "calibration.txt"

# Jeśli plik nie istnieje, twórz go z wartością 30.0
if not os.path.exists(CALIBRATION_FILE):
    with open(CALIBRATION_FILE, 'w') as f:
        f.write("30.0")

# Wczytaj wartość z pliku
with open(CALIBRATION_FILE, 'r') as f:
    try:
        calibration_value = float(f.read().strip())
    except ValueError:
        calibration_value = 30.0  # fallback jeśli plik uszkodzony

TimeToMaxDown = Value('d', calibration_value)
#proc = multiprocessing.Process(target=channel1Thread(), args=())

backProc = None
#nazwy Gpio są złe np pin 26 to GPIO 26
pins = {
    26 : {'name' : 'GPIO 5', 'state' : GPIO.LOW}, #uzywany
    19 : {'name' : 'GPIO 6', 'state' : GPIO.LOW},#uzywany
    8 : {'name' : 'GPIO 13', 'state' : GPIO.LOW},#uzywany
    20 : {'name' : 'GPIO 16', 'state' : GPIO.LOW},#uzywany
    1 : {'name' : 'GPIO 19', 'state' : GPIO.LOW},#uzywany
    21 : {'name' : 'GPIO 20', 'state' : GPIO.LOW},#uzywany
    17 : {'name' : 'GPIO 21', 'state' : GPIO.HIGH},#uzywany
    5 : {'name' : 'GPIO 26', 'state' : GPIO.HIGH},#uzywany
    13 : {'name' : 'GPIO 13', 'state' : GPIO.HIGH}, #uzywany
    9 : {'name' : 'GPIO 16', 'state' : GPIO.HIGH},#uzywany
    0 : {'name' : 'GPIO 19', 'state' : GPIO.HIGH},#uzywany
    10 : {'name' : 'GPIO 20', 'state' : GPIO.HIGH},#uzywany
    30 : {'name' : 'GPIO 21', 'state' : GPIO.HIGH},#nie uzywany
    3 : {'name' : 'GPIO 26', 'state' : GPIO.HIGH},#uzywany
    23 : {'name' : 'GPIO 13', 'state' : GPIO.HIGH}, #nie używany
    25 : {'name' : 'GPIO 16', 'state' : GPIO.HIGH}, #uzywant
}
buttons={
    14: {'name': 'GPIO 14', 'state': GPIO.LOW},  # przycisk 1
    15: {'name': 'GPIO 15', 'state': GPIO.LOW},  # przycisk 2
    18: {'name': 'GPIO 18', 'state': GPIO.LOW}  # Przycisk 3
}



# Konfiguracja pinów jako wejścia z podciąganiem do VCC (pull-up)
for pin in buttons:
    GPIO.setup(pin, GPIO.IN, pull_up_down=GPIO.PUD_UP)

for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.HIGH)

@app.route("/calibration")
def calibration():
    def calibration_logic():

        # Krok 1: Schodzimy w dół, dopóki wszystkie przyciski nie są wciśnięte
        print("Kalibracja: schodzę w dół...")
        ch1_down()
        ch2_down()
        ch3_down()

        while not all_buttons_pressed():
            time.sleep(0.1)

        # Zatrzymujemy wszystkie kanały
        mode_1()
        print("Wszystkie przyciski wciśnięte. Teraz jadę w górę przez 30s")

        # Krok 2: W górę przez 30 sekund
        ch1_up()
        ch2_up()
        ch3_up()
        time.sleep(20)
        mode_1()

        # Krok 3: W dół i mierzymy czas aż znowu wciśnięte zostaną wszystkie przyciski
        print("Rozpoczynam zjazd w dół i pomiar czasu")
        ch1_down()
        ch2_down()
        ch3_down()

        start_time = time.time()
        while not all_buttons_pressed():
            time.sleep(0.1)

        end_time = time.time()
        duration = end_time - start_time
        print(f"Czas powrotu na dół: {duration:.2f} sekundy")
        TimeToMaxDown.value = duration

        # Zapis do pliku
        with open(CALIBRATION_FILE, 'w') as f:
            f.write(f"{duration:.2f}")
        # Zatrzymanie aktuatorów
        mode_1()

    # Uruchamiamy jako proces równoległy by nie blokować serwera
    global backProc
    backProc = multiprocessing.Process(target=calibration_logic, daemon=True)
    backProc.start()

    return render_template('index.html'), 200


@app.route('/TimeToMaxDown')
def show_time_to_max_down():

    print(f"Maksymalny czas:{TimeToMaxDown.value}")
    return render_template('index.html'), 200

@app.route('/')
def hello_world():
  #  print("Started a background process with PID " + str(backProc.pid) + " is running: " + str(backProc.is_alive()))
    proc = multiprocessing.active_children()
    arr = []
    for p in proc:
        arr.append(p.pid)
    return render_template('index.html')

@app.route("/prog1")
def prog1():
    backProc = multiprocessing.Process(target=channel1Thread, args=(), daemon=True)
    backProc.start()
    backProc = multiprocessing.Process(target=channel2Thread, args=(), daemon=True)
    backProc.start()
    backProc = multiprocessing.Process(target=channel3Thread, args=(), daemon=True)
    backProc.start()
    backProc = multiprocessing.Process(target=vibRand, args=(), daemon=True)
    backProc.start()
    return render_template('index.html'),200

@app.route("/prog2")
def prog2():
    global backProc
    backProc = multiprocessing.Process(target=mode_2, args=(), daemon=True)
    backProc.start()
    return render_template('index.html'),200

@app.route("/prog3")
def prog3():
    global backProc
    backProc = multiprocessing.Process(target=mode_3, args=(), daemon=True)
    backProc.start()
    return render_template('index.html'),200


@app.route("/acc1/up")
def acc1Up():
    ch1_stop()
    ch1_up()
    return render_template('index.html')

@app.route("/acc1/down")
def acc1Down():
    ch1_stop()
    ch1_down()
    return render_template('index.html')

@app.route("/acc2/up")
def acc2Up():
    ch2_stop()
    ch2_up()
    return render_template('index.html')

@app.route("/acc2/down")
def acc2Down():
    ch2_stop()
    ch2_down()
    return render_template('index.html')

@app.route("/acc3/up")
def acc3Up():
    ch3_stop()
    ch3_up()
    return render_template('index.html')

@app.route("/acc3/down")
def acc3Down():
    ch3_stop()
    ch3_down()
    return render_template('index.html')

@app.route("/vib/start")
def vibStart():
    vibRun()
    return render_template('index.html')

@app.route("/vib/stop")
def vibStop():
    vibTerm()
    return render_template('index.html')

@app.route("/acc1/stop")
def acc1Stop():

    ch1_stop()
    ch2_stop()
    ch3_stop()
    vibTerm()
    return render_template('index.html')

@app.route("/all/down")
def allDownThread():
    backProc = multiprocessing.Process(target=allDown, args=(), daemon=True)
    backProc.start()
    return render_template('index.html')

def allDown():
    ch1_down()
    ch2_down()
    ch3_down()
    time.sleep(5)

@app.route("/all/up")
def allUpThread():
    backProc = multiprocessing.Process(target=allUp, args=(), daemon=True)
    backProc.start()
    return render_template('index.html')

def allUp():
    ch1_up()
    ch2_up()
    ch3_up()
    time.sleep(5)

@app.route("/halt")
def halt():
    proc = multiprocessing.active_children()
    for p in proc:
        p.terminate()
    mode_1()
    return render_template('index.html')

def ch1_down():
    ch1_stop()
    state = GPIO.LOW
    GPIO.output(26, state) #25
    GPIO.output(19, state) #24

def ch1_stop():
    state = GPIO.HIGH
    GPIO.output(26, state)
    GPIO.output(19, state)
    GPIO.output(8, state)
    GPIO.output(20, state)

def ch1_up():
    ch1_stop()
    state = GPIO.LOW
    GPIO.output(8, state) #10
    GPIO.output(20, state) #28


def ch2_down():
    ch2_stop()
    state = GPIO.LOW
    GPIO.output(1, state) #31
    GPIO.output(21, state) #29

def ch2_stop():
    state = GPIO.HIGH
    GPIO.output(1, state)
    GPIO.output(21, state)
    GPIO.output(25, state)
    GPIO.output(17, state)

def ch2_up():
    ch2_stop()
    state = GPIO.LOW
    GPIO.output(17, state) #0
    GPIO.output(25, state) #6

def ch3_down():
    ch3_stop()
    state = GPIO.LOW
    GPIO.output(5, state) #21
    GPIO.output(13, state) #23

def ch3_stop():
    state = GPIO.HIGH
    GPIO.output(5, state)
    GPIO.output(13, state)
    GPIO.output(9, state)
    GPIO.output(0, state)

def ch3_up():
    ch3_stop()
    state = GPIO.LOW
    GPIO.output(9, state) #13
    GPIO.output(0, state) #30

def vibRun():
    GPIO.output(10, GPIO.LOW) #12
    GPIO.output(3, GPIO.HIGH)
def vibTerm():
    GPIO.output(10, GPIO.HIGH) #12
    GPIO.output(3, GPIO.LOW)

def mode_1():
    ch1_stop()
    ch2_stop()
    ch3_stop()
def mode_2():
    while True:
        ch1_up()
        time.sleep(1)
        ch2_up()
        ch1_down()
        time.sleep(1)
        ch1_up()
        ch2_down()
        time.sleep(1)
        ch1_down()
        time.sleep(1)

def mode_3():
    while True:
        ch1_up()
        time.sleep(3)
        ch2_up()
        ch1_down()
        time.sleep(3)
        ch1_up()
        ch2_down()
        time.sleep(3)
        ch1_down()
        time.sleep(3)

def vibRand():
        vibRun()
        time.sleep(0.5)
        vibTerm()
        vibRun()
        time.sleep(0.7)
        vibTerm()
        vibRun()
        time.sleep(0.3)
        vibTerm()
        vibRun()
        time.sleep(1)
        vibTerm()
        vibRun()
        time.sleep(0.2)
        vibTerm()


def channel1Thread():
    while True:
        ch1_up()
        time.sleep(2)
        ch1_down()
        time.sleep(1)
        ch1_up()
        time.sleep(1)
        ch1_down()
        time.sleep(2)
        ch1_down()
    pass

def channel2Thread():
    while True:
        ch2_up()
        time.sleep(1)
        ch2_down()
        time.sleep(2)
        ch2_up()
        time.sleep(2)
        ch2_down()
        time.sleep(1)
    pass
def channel3Thread():
    while True:
        ch3_up()
        time.sleep(2)
        ch3_down()
        time.sleep(1)
        ch3_up()
        time.sleep(1)
        ch3_down()
        time.sleep(2)
    pass


def button1():
    return GPIO.input(14) == GPIO.HIGH  # Przycisk naciśnięty gdy LOW

def button2():
    return GPIO.input(15) == GPIO.HIGH

def button3():
    return GPIO.input(18) == GPIO.HIGH

def all_buttons_pressed():
    return button1() and button2() and button3()

def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

def stop_device(device):
    if device == 'acc1':
        ch1_stop()
    elif device == 'acc2':
        ch2_stop()
    elif device == 'acc3':
        ch3_stop()

def move_device(device, direction):
    if device == 'acc1':
        ch1_up() if direction == 'up' else ch1_down()
    elif device == 'acc2':
        ch2_up() if direction == 'up' else ch2_down()
    elif device == 'acc3':
        ch3_up() if direction == 'up' else ch3_down()

def move_one_by_percent(device,percent):
    with device_positions[device].get_lock():
        current = device_positions[device].value

    if percent == current:
        return

    move_by_percent = percent - current
    direction = 'up' if move_by_percent > 0 else 'down'
    duration = abs(move_by_percent) / 100 * TimeToMaxDown.value

    stop_device(device)
    move_device(device, direction)
    time.sleep(duration)
    stop_device(device)

    with device_positions[device].get_lock():
        device_positions[device].value = percent

def move_two_by_percent(device1, device2, percent):
    durations = {}
    directions = {}

    print(f"Moving {device1} and {device2} to {percent}%")

    for device in [device1, device2]:
        with device_positions[device].get_lock():
            current = device_positions[device].value
            durations[device] = abs(percent - current) / 100 * TimeToMaxDown.value
            directions[device] = 'up' if percent > current else 'down'

    for device in [device1, device2]:
        stop_device(device)
        move_device(device, directions[device])

    time.sleep(max(durations.values()))

    for device in [device1, device2]:
        stop_device(device)
        with device_positions[device].get_lock():
            device_positions[device].value = percent

    print(f"{device1} and {device2} are now at {percent}%")

def move_all_by_percent(percent):
    durations = {}
    directions = {}

    print("Positions before move:")
    for device in device_positions:
        with device_positions[device].get_lock():
            print(f"{device}: {device_positions[device].value}%")

    for device in device_positions:
        with device_positions[device].get_lock():
            current = device_positions[device].value
            durations[device] = abs(percent - current) / 100 * TimeToMaxDown.value
            directions[device] = 'up' if percent > current else 'down'

    for device in device_positions:
        stop_device(device)
        move_device(device, directions[device])

    time.sleep(max(durations.values()))

    for device in device_positions:
        stop_device(device)
        with device_positions[device].get_lock():
            device_positions[device].value = percent

    print("\nPositions after move:")
    for device in device_positions:
        with device_positions[device].get_lock():
            print(f"{device}: {device_positions[device].value}%")

device_positions = {
    'acc1': Value('d', 0.0),
    'acc2': Value('d', 0.0),
    'acc3': Value('d', 0.0)
}

@app.route('/api/control', methods=['POST'])
def control_device():
    data = request.get_json()

    if not data or 'device' not in data or 'action' not in data:
        return jsonify({'status': 'error', 'message': 'Invalid JSON data'}), 400

    device = data['device']
    action = data['action']
    percent = data.get('percent')

    try:
        if device not in device_positions and device not in ['vib', 'all']:
            return jsonify({'status': 'error', 'message': f'Unknown device: {device}'}), 400

        if device in device_positions:
            if action == 'up':
                stop_device(device)
                move_device(device, 'up')
            elif action == 'down':
                stop_device(device)
                move_device(device, 'down')
            elif action == 'stop':
                stop_device(device)
            elif action == 'percent':
                if percent is None or not (0 <= percent <= 100):
                    return jsonify({'status': 'error', 'message': 'Invalid percent value'}), 400

                move_one_by_percent(device,percent)

                return jsonify({'status': 'ok', 'message': f'{device} moved to {percent}%'}), 200

        elif device == 'vib':
            if action == 'start':
                vibRun()
            elif action == 'stop':
                vibTerm()

        elif device == 'all':
            if action == 'up':
                multiprocessing.Process(target=allUp, daemon=True).start()
            elif action == 'down':
                multiprocessing.Process(target=allDown, daemon=True).start()
            elif action == 'percent':
                if percent is None or not (0 <= percent <= 100):
                    return jsonify({'status': 'error', 'message': 'Invalid percent value'}), 400

                move_all_by_percent(percent)
                return jsonify({'status': 'ok', 'message': f'all moved to {percent}%'}), 200

        return jsonify({'status': 'ok', 'message': f'{device} {action} executed'}), 200

    except Exception as e:
        return jsonify({'status': 'error', 'message': str(e)}), 500

@app.route('/api/control/two', methods=['POST'])
def control_two_devices():
    data = request.get_json()

    device1 = data.get('device1')
    device2 = data.get('device2')
    percent = data.get('percent')

    if not device1 or not device2 or percent is None or device1 not in device_positions or device2 not in device_positions:
        return jsonify({'status': 'error', 'message': 'Invalid devices or percent'}), 400

    move_two_by_percent(device1, device2, percent)
    return jsonify({'status': 'ok', 'message': f'{device1} and {device2} moving to {percent}%'}), 200

@app.route('/upload', methods=['POST'])
def upload_file():
    if 'file' not in request.files:
        return jsonify({"success": False, "message": "No file part"}), 400

    file = request.files['file']
    if file.filename == '':
        return jsonify({"success": False, "message": "No selected file"}), 400

    filepath = os.path.join(os.getcwd(), file.filename)

    try:
        file.save(filepath)
        print(f"Saved file: {filepath}")
        threading.Thread(target=generate_report, args=(file.filename,)).start()
        return jsonify({"success": True, "message": f"File saved as {file.filename}"}), 200
    except Exception as e:
        return jsonify({"success": False, "message": str(e)}), 500

if __name__ == '__main__':
    app.run(host = getNetworkIp(), port=80)
