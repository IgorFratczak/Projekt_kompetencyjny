import requests

RASPBERRY_IP = '172.22.112.1'
API_URL = f'http://{RASPBERRY_IP}/api/control'

def send_command(device, action):
    try:
        payload = {
            "device": device,
            "action": action
        }

        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print("Done:", response.json()['message'])
        else:
            print("Error:", response.status_code, response.text)
    except Exception as e:
        print("Connection error:", e)

def print_commands():
    print("\nCommands:")
    print("  acc1 up / down / stop")
    print("  acc2 up / down / stop")
    print("  acc3 up / down / stop")
    print("  vib start / stop")
    print("  all up / down")
    print("  halt")
    print("  exit\n")

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

        try:
            device, action = cmd.split()
            send_command(device, action)
        except ValueError:
            print("Unknown command")

if __name__ == "__main__":
    main()
