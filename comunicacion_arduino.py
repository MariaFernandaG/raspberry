#!/usr/bin/env python3
import serial
import time

if __name__ == '__main__':
    ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
    ser.flush()
    while True:
        ser.write(b"Hello from Raspberry Pi!\n")
        line = ser.readline().decode('utf-8').rstrip()
        print(line)
        time.sleep(1)
        
# 
# if __name__ == '__main__':
#     try:
#         ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
#         ser.flush()
#         while True:
#             print("Insertar opción: oxigeno, temperatura o altura")
#             medicion = input()
#             #print(medicion)
#             if medicion == "temperatura":
#                 print("Medir temperatura")
#                 #medicionTemperatura()
#             elif medicion == "altura":
#                 print("Medir altura")
#                 #medicionAltura()
#             elif medicion == "oxigeno":
#                 print("Medir oxigeno")
#                 ser.write(b"oxigeno\n")
#                 line = ser.readline().decode('utf-8').rstrip()
#                 print(line)
#                 time.sleep(1)
#             elif medicion == "peso":
#                 print("Medir peso")
#                 ser.write(b"peso\n")
#                 line = ser.readline().decode('utf-8').rstrip()
#                 print(line)
#                 time.sleep(1)
#             else:
#                 print("Instrucción no válida")
# 
#      # Reset by pressing CTRL + C
#     except KeyboardInterrupt:
#         print("Measurement stopped by User")
#         GPIO.cleanup()