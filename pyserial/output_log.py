import serial
from datetime import datetime
ser = serial.Serial('/dev/ttyACM0')
print(ser.name)

while(1):
    hour = datetime.now().strftime("%Y%m%d-%H")
    minute = datetime.now().strftime("%Y%m%d-%H:%M")
    filename = "/home/pi/ws/wind_sensor/pyserial/logs/windspeed-" + hour + ".txt"
    with open(filename, "a") as f:
        f.write(minute + "," + str(ord(ser.read())) + "\n")
