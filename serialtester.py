import serial

ser = serial.Serial('/dev/rfcomm0')  # open serial port
print(ser.name)         # check which port was really used
print(ser.read(64))

ser.close()             # close port