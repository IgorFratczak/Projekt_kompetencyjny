import time
import requests
import threading

RASPBERRY_IP = '172.20.10.10'
API_URL = f'http://{RASPBERRY_IP}/api/control'

UNITY_IP = '192.168.137.88'
UNITY_PORT = 5000
UNITY_URL = f'http://{UNITY_IP}:{UNITY_PORT}/'

BACK = "acc1"
LEFT = "acc2"
RIGHT = "acc3"

actuator_state = {
    BACK: 0,
    LEFT: 0,
    RIGHT: 0
}

stop_requested = False
scenario_thread = None

def check_stop():
    if stop_requested:
        try:
            halt_response = requests.get(f'http://{RASPBERRY_IP}/halt')
            print("Done:", halt_response.status_code)
        except Exception as e:
            print("Error:", e)
        raise KeyboardInterrupt

def check_if_stopped(func):
    def wrapper(*args, **kwargs):
        check_stop()
        return func(*args, **kwargs)
    return wrapper

def get_calibrated_duration(device,percent):
    try:
        if device == BACK:
            with open("back_calibration.txt", "r") as f:
                max_duration = float(f.readline().strip())
                duration = max_duration * (abs(percent) / 100.0)
                return duration
        else:
            with open("calibration.txt", "r") as f:
                max_duration = float(f.readline().strip())
                duration = max_duration * (abs(percent) / 100.0)
                return duration
    except Exception as e:
        print("Error reading calibration.txt:", e)
        return 0

@check_if_stopped
def send_command(device, action, percent=None, save_state = False, save_pos = True):
    try:
        payload = {
            "device": device,
            "action": action
        }
        if percent is not None:
            if not (0 <= percent <= 100):
                print("Wrong percent: must be between 0 and 100")
                return
            payload['percent'] = percent
            payload['save_pos'] = save_pos
            if action == "percent" and save_state == True:
                if device == "all":
                    actuator_state[BACK] = percent
                    actuator_state[LEFT] = percent
                    actuator_state[RIGHT] = percent
                elif device in actuator_state:
                    actuator_state[device] = percent

        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("Done:", response.json()['message'])
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Connection error:", e)

@check_if_stopped
def send_command_two_devices(device1, device2, percent, save_state = False):
    try:
        if not (0 <= percent <= 100):
            print("Percent must be between 0 and 100")
            return

        payload = {
            "device1": device1,
            "device2": device2,
            "percent": percent
        }

        if device1 in actuator_state and save_state == True:
            actuator_state[device1] = percent
        if device2 in actuator_state and save_state == True:
            actuator_state[device2] = percent

        response = requests.post(f'http://{RASPBERRY_IP}/api/control/two', json=payload)
        if response.status_code == 200:
            print("Done:", response.json()['message'])
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Connection error:", e)

@check_if_stopped
def send_to_unity(payload):
    try:
        headers = {'Content-Type': 'application/json'}
        response = requests.post(UNITY_URL, json=payload, headers=headers)
        if response.status_code == 200:
            print("Sent to Unity:", payload)
        else:
            print("Failed to send to Unity:", response.status_code)
    except Exception as e:
        print("Error sending to Unity:", e)

def  move_actuators(percent, *devices):
    if not devices:
        print("No devices specified for move_actuators.")
        return

    for device in devices:
        previous_percent = actuator_state.get(device, 0)
        delta = percent - previous_percent

        duration = get_calibrated_duration(device,delta)

        unity_percent = 20 if delta > 0 else -20 if delta < 0 else 0

        print("prev %:", previous_percent ,"device", device, "delta", delta, "moving in unity by:", unity_percent)
        payload = {
            "command": "rotate_platform",
            "actuator_name": device,
            "percent": unity_percent/100,
            "duration": duration
        }
        send_to_unity(payload)

        actuator_state[device] = percent

    if len(devices) == 1:
        send_command(devices[0], "percent", percent, False)
    elif len(devices) == 2:
        send_command_two_devices(devices[0], devices[1], percent, False)


def print_commands():
    print("\nCommands:")
    print("  acc1 up / down / stop / percent (value)")
    print("  acc2 up / down / stop / percent (value)")
    print("  acc3 up / down / stop / percent (value)")
    print("  accX accY percent (value)")
    print("  all up / down / percent (value)")
    print("  halt")
    print("  turbulences loop_len (use only for debugging at height 10)")
    print("  calibrate back")
    print("  scenario easy")
    print("  scenario medium")
    print("  scenario hard")
    print("  stop")
    print("  exit\n")

@check_if_stopped
def turbulences(loop_length):
    send_command("vib", "start")
    # time.sleep(loop_length)
    # send_command("vib", "stop")

    base_left = actuator_state[LEFT]
    base_right = actuator_state[RIGHT]
    base_back = actuator_state[BACK]

    for _ in range(loop_length):
        check_stop()
        send_command(LEFT, "percent", base_left + 0.2)
        send_command(RIGHT, "percent", base_right + 0.2)
        send_command(BACK, "percent", base_back + 0.2)

        send_command(LEFT, "percent", base_left)
        send_command(RIGHT, "percent", base_right)
        send_command(BACK, "percent", base_back)
    send_command("vib", "stop")
    send_command(RIGHT, "percent", base_back + 0.5,save_pos = False)
    send_command(LEFT, "percent", base_back + 0.5,save_pos = False)
    send_command(BACK, "percent", base_back + 0.9,save_pos = False)

    actuator_state[LEFT] = base_left
    actuator_state[RIGHT] = base_right
    actuator_state[BACK] = base_back

def scenario_easy():
    print("Running scenario: easy\n")
    send_command("all", "percent", 0)
    send_command("all","down")

    time.sleep(3)

    send_to_unity({"command": "set_flag", "type": 1})
    send_to_unity({"command": "set_time", "time": "day"})
    send_to_unity({"command": "start_face_tracking"})
    send_to_unity({"command": "play_sound", "sound_name": "flight"})

    # Dźwięk startu
    send_to_unity({"command": "play_sound", "sound_name": "take_off"})
    send_command("vib", "start")
    time.sleep(34)

    move_actuators(10, LEFT, RIGHT)
    time.sleep(15)

    # Stabilny lot
    move_actuators(10, BACK)
    time.sleep(15)
    send_command("vib", "stop")

    send_to_unity({"command": "set_flag", "type": 0})
    time.sleep(120)

    # Lądowanie
    send_to_unity({"command": "set_flag", "type": 3})
    send_to_unity({"command": "play_sound", "sound_name": "landing"})
    time.sleep(38)
    move_actuators(0, LEFT, RIGHT)
    time.sleep(15)
    move_actuators(0, BACK)

    time.sleep(10)
    send_to_unity({"command": "exit"})

    print("Scenario EASY completed.")

def scenario_medium():
    print("Running scenario: medium\n")
    send_command("all", "percent", 0)
    send_command("all","down")
    time.sleep(3)

    time.sleep(10)

    send_to_unity({"command": "set_flag", "type": 1})
    send_to_unity({"command": "set_time", "time": "day"})
    send_to_unity({"command": "start_face_tracking"})
    send_to_unity({"command": "play_sound", "sound_name": "flight"})

    # Dźwięk startu
    send_to_unity({"command": "play_sound", "sound_name": "take_off"})
    send_command("vib", "start")
    time.sleep(34)

    move_actuators(10, LEFT, RIGHT)
    time.sleep(15)

    # Stabilny lot
    move_actuators(10, BACK)
    time.sleep(15)
    send_command("vib", "stop")

    # Stabilny lot
    send_to_unity({"command": "set_flag", "type": 0})
    time.sleep(15)

    # Lekkie turbulencje
    print("Simulating light turbulence...")
    send_to_unity({"command": "set_flag", "type": 2})
    for _ in range(4):
        turbulences(loop_length=5)
    time.sleep(5)

    # Stabilny lot
    send_to_unity({"command": "set_flag", "type": 0})
    time.sleep(25)

    # Lekkie turbulencje
    print("Simulating light turbulence...")
    send_to_unity({"command": "set_flag", "type": 2})
    for _ in range(2):
        turbulences(loop_length=5)
    time.sleep(5)

    # Stabilny lot
    send_to_unity({"command": "set_flag", "type": 0})
    time.sleep(15)

    # Lądowanie
    send_to_unity({"command": "set_flag", "type": 3})
    send_to_unity({"command": "play_sound", "sound_name": "landing"})
    time.sleep(38)
    move_actuators(0, LEFT, RIGHT)
    time.sleep(15)
    move_actuators(0, BACK)

    time.sleep(10)
    send_to_unity({"command": "exit"})

    print("Scenario MEDIUM completed.")

def scenario_hard():
    print("Running scenario: hard\n")
    send_command("all", "percent", 0)
    send_command("all", "down")
    time.sleep(3)

    send_to_unity({"command": "set_flag", "type": 1})
    send_to_unity({"command": "set_time", "time": "day"})
    send_to_unity({"command": "start_face_tracking"})
    send_to_unity({"command": "play_sound", "sound_name": "flight"})

    # Start
    send_to_unity({"command": "play_sound", "sound_name": "take_off"})
    send_command("vib", "start")
    time.sleep(34)

    move_actuators(10, LEFT, RIGHT)
    time.sleep(15)

    move_actuators(10, BACK)
    time.sleep(15)
    send_command("vib", "stop")

    # Stabilny lot
    send_to_unity({"command": "set_flag", "type": 0})
    time.sleep(15)

    # Silne turbulencje
    print("Simulating heavy turbulence...")
    send_to_unity({"command": "set_flag", "type": 2})
    for _ in range(3):
        for _ in range(4):
            turbulences(loop_length=5)
        time.sleep(5)

    # Stabilny lot
    send_to_unity({"command": "set_flag", "type": 0})
    time.sleep(20)

    # Lądowanie
    send_to_unity({"command": "set_flag", "type": 3})
    send_to_unity({"command": "play_sound", "sound_name": "landing"})
    time.sleep(38)
    move_actuators(0, LEFT, RIGHT)
    time.sleep(15)
    move_actuators(0, BACK)

    time.sleep(10)
    send_command("all","down")
    send_to_unity({"command": "exit"})

    print("Scenario HARD completed.")

def send_calibration_to_server(value):
    try:
        url = f"http://{RASPBERRY_IP}/set_calibration"
        response = requests.post(url, json={"value": value})
        if response.status_code == 200:
            print("Wysłano kalibrację na serwer:", value)
        else:
            print("Błąd serwera:", response.text)
    except Exception as e:
        print("Nie udało się wysłać kalibracji:", e)

@check_if_stopped
def calibrate_back_time():
    send_calibration_to_server(30.0)

    send_command("all", "percent", 0)
    send_command("all", "down")

    input("Press ENTER when seat has been taken")
    target_percent = 10
    send_command_two_devices(LEFT,RIGHT,target_percent)

    print(f"Calibrating rear actuator to reach {target_percent}% like front actuators...")

    input("Press ENTER to start moving rear actuator (UP)...")
    send_command(BACK, "up")
    start_time = time.time()

    input(f"Press ENTER when rear actuator visually matches {target_percent}% level...")
    send_command(BACK, "stop")
    end_time = time.time()
    time.sleep(3)

    elapsed_time = end_time - start_time
    whole_time = elapsed_time * 10
    print(f"Measured time to reach ~{target_percent}%: {elapsed_time:.3f} seconds, whole time: {whole_time:.3f}")
    send_calibration_to_server(whole_time)
    send_command("all", "percent", 0)
    send_command("all", "down")

    try:
        with open("back_calibration.txt", "w") as f:
            f.write(f"{whole_time:.3f}\n")
        print("Saved back calibration time.")
    except Exception as e:
        print("Error saving back calibration time:", e)

def main():
    global stop_requested, scenario_thread

    print("Chair control")
    print("acc1 - back | acc2 - left | acc3 - right")
    print_commands()

    while True:
        cmd = input("> ").strip().lower()

        if cmd == "exit":
            break

        elif cmd == "help":
            print_commands()
            continue

        elif cmd == "calibrate back":
            calibrate_back_time()
            continue

        elif cmd == "halt":
            try:
                halt_response = requests.get(f'http://{RASPBERRY_IP}/halt')
                print("Done:", halt_response.status_code)
            except Exception as e:
                print("Error:", e)
            continue

        elif cmd.startswith("scenario"):
            if scenario_thread and scenario_thread.is_alive():
                print("Scenario is already running. Use 'stop' to interrupt.")
                continue

            stop_requested = False
            parts = cmd.split()
            if len(parts) != 2:
                print("Specify scenario: easy / medium / hard")
                continue
            scenario_name = parts[1]

            def run_scenario():
                try:
                    if scenario_name == "easy":
                        scenario_easy()
                    elif scenario_name == "medium":
                        scenario_medium()
                    elif scenario_name == "hard":
                        scenario_hard()
                    else:
                        print("Unknown scenario")
                except KeyboardInterrupt:
                    print("Scenario forcefully stopped.")
                    send_command("vib", "stop")
                    send_command("all", "percent", 0)

            scenario_thread = threading.Thread(target=run_scenario)
            scenario_thread.start()
            continue

        elif cmd == "stop":
            send_command("vib", "stop")
            stop_requested = True
            print("Stop requested. Waiting for scenario to halt...")
            if scenario_thread:
                scenario_thread.join()
                print("Scenario halted.")
            continue

        elif cmd.startswith("all "):
            parts = cmd.split()
            if len(parts) == 2:
                action = parts[1]
                if action in ("up", "down", "stop"):
                    send_command("all", action)
                else:
                    print("Unknown action for 'all':", action)
            elif len(parts) == 3:
                action, value = parts[1], parts[2]
                if action == "percent":
                    try:
                        percent = int(value)
                        send_command("all", "percent", percent)
                    except ValueError:
                        print("Invalid percent value")
                else:
                    print("Unknown action for 'all':", action)
            else:
                print("Invalid 'all' command format")
            continue

        try:
            parts = cmd.split()
            if len(parts) == 2:
                if parts[0] == "turbulences":
                    for i in actuator_state:
                        actuator_state[i] = 10
                    turbulences(int(parts[1]))
                else:
                    device, action = parts
                    send_command(device, action)
            elif len(parts) == 3:
                device, action, value = parts
                if action == "percent":
                    percent = int(value)
                    send_command(device, action, percent)
                else:
                    print("Unknown command")
            elif len(parts) == 4:
                device1, device2, action, value = parts
                if device1 == device2:
                    print("Devices are the same")
                    continue
                if action == "percent":
                    percent = int(value)
                    send_command_two_devices(device1, device2, percent)
                else:
                    print("Unknown command")
            else:
                print("Unknown command")
        except Exception as e:
            print("Error:", e)

if __name__ == "__main__":
    main()