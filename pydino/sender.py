import serial, time
arduino = serial.Serial("COM3", 9600)
time.sleep(2)
arduino.write(b'ON')
while True:
    print("[1] On     [2] Off")
    ac = input(">> ")
    if ac == "1":
        arduino.write(b'ON')
    elif ac == "2":
        arduino.write(b'OFF')

arduino.close()
