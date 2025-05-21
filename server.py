from flask import Flask, Markup, render_template, request
from urllib.request import urlopen
import simplejson as json
import sys
import RPi.GPIO as GPIO
import time
import socket
import _thread as thread
import multiprocessing


app = Flask(__name__)
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

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
    25 : {'name' : 'GPIO 16', 'state' : GPIO.HIGH} #uzywant
}

for pin in pins:
   GPIO.setup(pin, GPIO.OUT)
   GPIO.output(pin, GPIO.HIGH)


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


def getNetworkIp():
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
    s.connect(('<broadcast>', 0))
    return s.getsockname()[0]

if __name__ == '__main__':
    app.run(host = getNetworkIp(), port=80)
