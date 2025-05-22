import time
import requests

RASPBERRY_IP = '192.168.192.229'
API_URL = f'http://{RASPBERRY_IP}/api/control'

UNITY_IP = '192.168.51.8'
UNITY_PORT = 5000
UNITY_URL = f'http://{UNITY_IP}:{UNITY_PORT}/'

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
    print("  acc1 up / down / stop / percent")
    print("  acc2 up / down / stop / percent")
    print("  acc3 up / down / stop / percent")
    print("  vib start / stop")
    print("  all up / down / percent")
    print("  halt")
    print("  scenario easy")
    print("  scenario medium")
    print("  scenario hard")

    print("  exit\n")

def scenario_easy():
    print("Running scenario: easy")
    send_scenario_to_unity("scenario easy")
    send_command("acc1", "up")
    time.sleep(1)
    send_command("acc1", "down")

def scenario_medium():
    print("Running scenario: medium")
    send_scenario_to_unity("scenario medium")
    send_command("vib", "start")
    time.sleep(0.5)
    send_command("vib", "stop")
    time.sleep(0.3)
    send_command("vib", "start")
    time.sleep(1)
    send_command("vib", "stop")

def scenario_hard():
    print("Running scenario: hard")
    send_scenario_to_unity("scenario hard")
    send_command("vib", "start")
    time.sleep(10)
    send_command("vib", "stop")

def main():
    print("Chair control")
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
            scenario_medium()
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
            else:
                print("Unknown command")
        except ValueError:
            print("Unknown command")

if __name__ == "__main__":
    main()
