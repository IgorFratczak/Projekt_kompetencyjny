from flask import Flask, Markup, render_template, request
from urllib.request import urlopen
import simplejson as json
import sys
import RPi.GPIO as GPIO
import time

app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

pins = {
    5 : {'name' : 'GPIO 5', 'state' : GPIO.HIGH},
    6 : {'name' : 'GPIO 6', 'state' : GPIO.HIGH},
    13 : {'name' : 'GPIO 13', 'state' : GPIO.HIGH},
    16 : {'name' : 'GPIO 16', 'state' : GPIO.HIGH},
    19 : {'name' : 'GPIO 19', 'state' : GPIO.HIGH},
    20 : {'name' : 'GPIO 20', 'state' : GPIO.HIGH},
    21 : {'name' : 'GPIO 21', 'state' : GPIO.HIGH},
    26 : {'name' : 'GPIO 26', 'state' : GPIO.HIGH}
}

for pin in pins:
    GPIO.setup(pin, GPIO.OUT)
    GPIO.output(pin, GPIO.HIGH)


@app.route('/')
def hello_world():
    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)
    # Put the pin dictionary into the template data dictionary:
    templateData = {
        'pins' : pins
    }
    # gpio_init()
    # ch1_up(3)
    return render_template('index.html', **templateData, title='System', max=40)

@app.route("/<changePin>/<action>")
def action(changePin, action):
    # Convert the pin from the URL into an integer:
    changePin = int(changePin)
    # Get the device name for the pin being changed:
    deviceName = pins[changePin]['name']
    # If the action part of the URL is "on," execute the code indented below:
    if action == "on":
        # Set the pin high:
        GPIO.output(changePin, GPIO.HIGH)
        # Save the status message to be passed into the template:
        message = "Turned " + deviceName + " on."
    if action == "off":
        GPIO.output(changePin, GPIO.LOW)
        message = "Turned " + deviceName + " off."

    # For each pin, read the pin state and store it in the pins dictionary:
    for pin in pins:
        pins[pin]['state'] = GPIO.input(pin)

    # Along with the pin dictionary, put the message into the template data dictionary:
    templateData = {
        'pins' : pins
    }

    return render_template('index.html', **templateData)


def ch1_up(time_up):
    GPIO.output(6, GPIO.HIGH)
    time.sleep(time_up)
    GPIO.output(6, GPIO.LOW)

def gpio_init():
    #set mode out
    GPIO.setup(5, GPIO.OUT)
    GPIO.setup(6, GPIO.OUT)
    GPIO.setup(13, GPIO.OUT)
    GPIO.setup(16, GPIO.OUT)
    GPIO.setup(19, GPIO.OUT)
    GPIO.setup(20, GPIO.OUT)
    GPIO.output(5, GPIO.LOW)
    GPIO.output(6, GPIO.LOW)
    GPIO.output(13, GPIO.LOW)
    GPIO.output(16, GPIO.LOW)
    GPIO.output(19, GPIO.LOW)
    GPIO.output(20, GPIO.LOW)

if __name__ == '__main__':
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(host='192.168.43.127', port= 80)
