#Código para medir altura con el sensor ultrasónico usando un botoón

#Libraries
import RPi.GPIO as GPIO
import time
from time import sleep

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


flag_sw = 0

global altura
altura = 0.00
refaltura = 0.00
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

#EQUIVALENTE A MILLIS() DE ARDUINO
millis = lambda: int(round(time.time() * 1000))

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
            button_state = GPIO.input(GPIO_BUTTON)
            #print(button_state) 

            if button_state == 0:   #is pressed
                pressedTime = millis()
                isPressing = 1
                #isLongDetected = 0
                flag_sw = 1
                while flag_sw == 1:
                    button_state = GPIO.input(GPIO_BUTTON)
                    #print("on")
                    if button_state == 1 and flag_sw == 1:
                        flag_sw = 0
                        isPressing = 0
                        releasedTime = millis()
                        
                        pressDuration = releasedTime - pressedTime
                        #print(pressDuration)
                        if pressDuration <  LONG_PRESS_TIME:
                            contador_on = contador_on + 1
                            #print(contador_on)
                            
                            if contador_on == 1:   
                                menu = 4
                                print("medir referencia")
                                        
                            if contador_on > 1:
                                menu = 5
                                print("medir altura")
                        elif pressDuration > LONG_PRESS_TIME:
                            print("REINICIAR")
                            menu = 0
                            contador_on = 0
                            flag_sw = 0
                                
                
#             if button_state == 1 and flag_sw == 1: #is released
#                 print("OFF")
#                 isPressing = 0
#                 releasedTime = millis()
#                 #print(button_state)
#                 flag_sw = 0
#                 pressDuration = releasedTime - pressedTime
#                 #print(pressDuration)
#                 
#                 if pressDuration <  LONG_PRESS_TIME:
#                     contador_on = contador_on + 1
#                     print(contador_on)
#                     
#                     if contador_on == 1:   
#                         menu = 4
#                         print("medir referencia")
#                                 
#                     if contador_on > 1:
#                         menu = 5
#                         print("medir altura")
#                 
#                 elif pressDuration > LONG_PRESS_TIME:   #APAGAR SI ESTÁ SOSTENIDO 
#                     print("REINICIAR")
#                     menu = 0
#                     contador_on = 0
#                     flag_sw = 0

                    
            
            if menu == 4:
                getAltura()
                refaltura = altura
                print(refaltura)
                menu = 0
                
            if menu == 5:
                getAltura()
                altura = refaltura - altura
                print(altura)
                menu = 0
            

# 
#             if button_state==0:
#                 sleep(0.5)
#                 if flag==0:
#                     flag=1 
#             else:
#                 flag=0
#             if flag==1:
#                 getAltura()
#                 print ("Measured Distance = %.1f cm" % altura)
#                 time.sleep(1)

     # Reset by pressing CTRL + C
    except KeyboardInterrupt:
        print("Measurement stopped by User")
        GPIO.cleanup()

