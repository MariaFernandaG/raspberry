#Código para medir temperatura cuando se está a una distancia entre 4 y 6 cm del sensor ultrasónico 

#Libraries
import RPi.GPIO as GPIO
import time
from time import sleep

#TEMPERATURA
import board
import adafruit_mlx90614

GPIO.setwarnings(False)
#GPIO Mode (BOARD / BCM)
GPIO.setmode(GPIO.BCM)


#set GPIO Pins
GPIO_TRIGGER = 18
GPIO_ECHO = 24
GPIO_BUTTON = 16

#set GPIO direction (IN / OUT)
GPIO.setup(GPIO_TRIGGER, GPIO.OUT)
GPIO.setup(GPIO_ECHO, GPIO.IN)
GPIO.setup(GPIO_BUTTON, GPIO.IN,pull_up_down = GPIO.PUD_UP)


#VARIABLES ALTURA
flag_sw = 0

global altura
altura = 0.0
refaltura = 0.0
contador_on = 0
contador_sw = 0
menu = 0
pressedTime  = 0;
releasedTime = 0;
pressDuration = 0;

LONG_PRESS_TIME  = 8000    #miliseconds
SHORT_PRESS_TIME = 1000

isPressing = 0
isLongDetected = 0

#VARIABLES TEMPERATURA
global promedioTemperatura
promedioTemperatura = 0.0

distance = 0.0;
distanceValid = 0
#temps, tempc, tempa, temperature;


#EQUIVALENTE A MILLIS() DE ARDUINO
millis = lambda: int(round(time.time() * 1000))
def readTemperatura():
    global promedioTemperatura
    promedioTemperatura = 0.0
    i2c = board.I2C()
    mlx = adafruit_mlx90614.MLX90614(i2c)
    temp = 0.0
    tLow = 0.0
    tHigh = 0.0
    TA = 0.0
    TF = 0.0
    TCore = 0.0
    varTemp = 0.007358834
    varProcess = 1e-9
    Pc = 0.0
    G = 0.0
    P = 1.0
    Xp = 0.0
    Zp = 0.0
    Xe = 0.0
    
    for i in range(10):
        temp = mlx.object_temperature
        
        while temp < 0 or temp > 45:
            print("Sensor no responde")
            #mlx.writeEmissivity(0.98);
            time.sleep(100)
            temp = mlx.object_temperature
            print(temp)
            
        
        #FILTRO KALMAN
        Pc = P + varProcess
        G = Pc / (Pc + varTemp)
        P = (1 - G) * Pc
        Xp = Xe
        Zp = Xp
        Xe = G * (temp - Zp) + Xp
        time.sleep(0.01)      #delay de 10ms
    
    TA = mlx.ambient_temperature
    
    if TA <= 25:
        tLow =  32.66 + 0.186 * (TA - 25)
        tHigh = 34.84 + 0.148 * (TA - 25)
    if TA > 25:
        tLow =  32.66 + 0.086 * (TA - 25)
        tHigh = 34.84 + 0.100 * (TA - 25)
        
    TF = Xe
    
    if TF < tLow:
        TCore = 36.3 + (0.551658273 + 0.021525068 * TA) * (TF - tLow)
    if tLow < TF and TF < tHigh:
        TCore = 36.3 + 0.5 / (tHigh - tLow) * (TF - tLow)
    if TF > tHigh:
        TCore = 36.8 + (0.829320618 + 0.002364434 * TA) * (TF - tHigh)
        
    promedioTemperatura = TCore
    print("TempAmb: ", TA)
    print("TL: ", tLow)
    print("TH: ", tHigh)
    print("TF: ", TF)
    print("TCore: ", TCore)
 
def readAltura():
    # set Trigger to HIGH
    GPIO.output(GPIO_TRIGGER, True)

    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(GPIO_TRIGGER, False)

    StartTime = time.time()
    StopTime = time.time()

    # save StartTime
    while GPIO.input(GPIO_ECHO) == 0:
        StartTime = time.time()

    # save time of arrival
    while GPIO.input(GPIO_ECHO) == 1:
        StopTime = time.time()

    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
    #distance = TimeElapsed * 0.01715

    return distance


def getAltura():
    global altura
    varDistance = 0.0567274773869351   #variance determined using excel and reading samples of raw sensor data
    varProcessD = 1e-8
    temp = 0.0
    prom = 0
    PcD = 0.0
    GD = 0.0
    PD = 1.0
    XpD = 0.0
    ZpD = 0.0
    XeD = 0.0
     
    for i in range(25):
        temp = round( readAltura())
        prom += temp
    
        #Filtro Kalman
        PcD = PD + varProcessD
        GD = PcD / (PcD + varDistance)
        PD = (1 - GD) * PcD
        XpD = XeD
        ZpD = XpD
        XeD = GD * (temp - ZpD) + XpD
        time.sleep(0.01)      #delay de 10ms
    prom /= 25
    prom += 1
    altura = (XeD) + 1


if __name__ == '__main__':
    try:
        while True:
#             getAltura()
#             distance = altura
#             print(distance)
            while distanceValid == 0:               
                getAltura()
                distance = altura
                #print(distance)
                if distance > 4 and distance <= 6:
                    distanceValid = 1
                else:
                    distanceValid = 0
            
            if distanceValid == 1:
                readTemperatura()
                if  promedioTemperatura > 34 and promedioTemperatura < 42.1:
                    print("Temperatura: ",promedioTemperatura)
                else:
                    print("Temperatura fuera de los límites")
                    print(distance)
            distanceValid = 2
            
            

     # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()