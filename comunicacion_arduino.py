#ENVIO DE DATOS ENTRE RASPBERRY Y ARDUINO NANO (SERIAL)
import serial
import time

#VARIABLES OXIGENO
flag_ox = 0
flag_peso = 0

# if __name__ == '__main__':
#     ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
#     ser.flush()
#     while True:
#         ser.write(b"Hello from Raspberry Pi!\n")
#         line = ser.readline().decode('utf-8').rstrip()
#         print(line)
#         time.sleep(1)
        

if __name__ == '__main__':
    try:
        ser = serial.Serial('/dev/ttyUSB0', 115200, timeout=1)
        ser.flush()
        while True:
            print("Insertar opción: oxigeno, temperatura, altura o peso")
            medicion = input()
            #print(medicion)
            if medicion == "temperatura":
                print("Medir temperatura")
                #medicionTemperatura()
            elif medicion == "altura":
                print("Medir altura")
                #medicionAltura()
            elif medicion == "oxigeno":
                print("Medir oxigeno")
                flag_ox = 1
                ser.write(b"oxigeno\n")
                while flag_ox == 1:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').rstrip() 
                        print(line)
                        #time.sleep(1)
            elif medicion == "peso":
                print("Medir peso")
                flag_peso = 1
                ser.write(b"peso\n")
                while flag_peso == 1:
                    if ser.in_waiting > 0:
                        line = ser.readline().decode('utf-8').rstrip() 
                        #print(line)
                        if line == "finp":
                            line = ser.readline().decode('utf-8').rstrip()
                            print(line)
                            flag_peso = 0
                            
            else:
                print("Instrucción no válida")

     # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()