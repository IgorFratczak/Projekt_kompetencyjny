import time
import requests

RASPBERRY_IP = '192.168.229.229'
API_URL = f'http://{RASPBERRY_IP}/api/control'

UNITY_IP = '192.168.51.8'
UNITY_PORT = 5000
UNITY_URL = f'http://{UNITY_IP}:{UNITY_PORT}/'

BACK = "acc1"
LEFT = "acc2"
RIGHT = "acc3"

# acc1 - back | acc2 - left | acc3 - right
def send_command(device, action,percent = None):
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

        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("Done:", response.json()['message'])
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Connection error:", e)

def send_command_two_devices(device1, device2, percent):
    try:
        if not (0 <= percent <= 100):
            print("Percent must be between 0 and 100")
            return

        payload = {
            "device1": device1,
            "device2": device2,
            "percent": percent
        }
        response = requests.post(f'http://{RASPBERRY_IP}/api/control/two', json=payload)
        if response.status_code == 200:
            print("Done:", response.json()['message'])
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Connection error:", e)

def send_scenario_to_unity(scenario_name):
    try:
        response = requests.post(UNITY_URL, data=scenario_name)
        if response.status_code == 200:
            print(f"Sent scenario '{scenario_name}' to Unity")
        else:
            print(f"Failed to send scenario to Unity: {response.status_code}")
    except Exception as e:
        print("Error sending to Unity:", e)

def print_commands():
    print("\nCommands:")
    print("  acc1 up / down / stop / percent (value)")
    print("  acc2 up / down / stop / percent (value)")
    print("  acc3 up / down / stop / percent (value)")
    print("  accX accY percent (value)")
    print("  vib start / stop")
    print("  all up / down / percent (value)")
    print("  halt")
    print("  scenario easy")
    print("  scenario medium")
    print("  scenario hard")

    print("  exit\n")

def turbulences(loop_length,percent):
    send_command("vib", "start")
    for _ in range(loop_length):
        send_command(LEFT, "percent", percent + 1)
        send_command(RIGHT, "percent", percent + 1)
        send_command(BACK, "percent", percent + 1)

        send_command(LEFT, "percent", percent)
        send_command(RIGHT, "percent", percent)
        send_command(BACK, "percent", percent)
    send_command("vib", "stop")

def scenario_easy():
    print("Running scenario: easy")
    send_command("all", "percent", 0)
    #send_scenario_to_unity("scenario easy")

    # Start lotu
    send_command("vib", "start")
    time.sleep(1)
    send_command("vib", "stop")

    send_command_two_devices(LEFT, RIGHT, 20)
    time.sleep(8)

    # Stabilny lot
    send_command("all", "percent", 20)
    time.sleep(20)

    # Lądowanie
    send_command_two_devices(LEFT, RIGHT, 0)
    time.sleep(8)
    send_command(BACK, "percent", 0)


def scenario_medium():
    print("Running scenario: medium")
    send_command("all", "percent", 0)
    #send_scenario_to_unity("scenario medium")

    # Start lotu
    send_command("vib", "start")
    time.sleep(2)
    send_command_two_devices(LEFT, RIGHT, 30)
    time.sleep(10)
    send_command("vib", "stop")

    # Stabilny lot
    send_command("all", "percent", 30)
    time.sleep(10)

    # Lekkie turbulencje
    print("Simulating light turbulence")
    send_command("vib", "start")
    time.sleep(4)
    send_command("vib", "stop")

    time.sleep(10)

    # Lądowanie
    send_command_two_devices(LEFT, RIGHT, 0)
    time.sleep(10)
    send_command(BACK, "percent", 0)


def scenario_hard():
    print("Running scenario: hard")
    send_command("all", "percent", 0)

    # Start lotu
    send_command("vib", "start")
    send_command_two_devices(LEFT, RIGHT, 20)
    time.sleep(1)
    send_command("vib", "stop")

    # Stabilny lot
    send_command("all", "percent", 20)
    time.sleep(3)

    # Turbulencje
    # for _ in range(3):
    #     send_command("vib", "start")
    #     time.sleep(5)
    #     send_command("vib", "stop")
    #     time.sleep(2)

    # for _ in range(10):
    #     send_command("vib", "start")
    #     time.sleep(1)
    #     send_command("vib", "stop")
    #     time.sleep(0.5)
    turbulences(10,20)

    # Stabilizacja
    time.sleep(10)

    # Lądowanie
    send_command_two_devices(LEFT, RIGHT, 0)
    time.sleep(12)
    send_command(BACK, "percent", 0)


def main():
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
        elif cmd == "halt":
            try:
                halt_response = requests.get(f'http://{RASPBERRY_IP}/halt')
                print("Done:", halt_response.status_code)
            except Exception as e:
                print("Error:", e)
            continue
        elif cmd == "scenario easy":
            scenario_easy()
            continue
        elif cmd == "scenario medium":
            scenario_medium()
            continue
        elif cmd == "scenario hard":
            scenario_hard()
            continue
        try:
            parts = cmd.split()
            if len(parts) == 2:
                device, action = parts
                send_command(device, action)
            elif len(parts) == 3:
                device, action, value = parts
                if action == "percent":
                    try:
                        percent = int(value)
                        send_command(device, action, percent)
                    except ValueError:
                        print("Invalid percent value")
                else:
                    print("Unknown command")
            elif len(parts) == 4:
                device1,device2,action,value = parts
                if device1 == device2:
                    print("Devices are the same")
                    continue
                if action == "percent":
                    try:
                        percent = int(value)
                        send_command_two_devices(device1,device2, percent)
                    except ValueError:
                        print("Invalid percent value")
                else:
                    print("Unknown command")
            else:
                print("Unknown command")
        except ValueError:
            print("Unknown command")

if __name__ == "__main__":
    main()
