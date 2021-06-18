# CONFIGURACIÓN RASPBERRY PI 4


## Instalar VNC Viewer 

- sudo apt update

- sudo apt install realvnc-vnc-server realvnc-vnc-viewer

## Librerías

### RPi.GPIO

- sudo apt-get update

- sudo apt-get install rpi.gpio

### adafruit_mlx90614

- pip3 install adafruit-circuitpython-mlx90614

- sudo pip3 install adafruit-circuitpython-mlx90614

### board

- pip install board

### serial

- python3 -m pip install pyserial

### VL53L1X

- sudo pip3 install smbus

- sudo pip3 install vl53l1x 

### REDIS 

- pip3 install redis

- pip3 install getmac 

## HABILIRAR COMUNICACIÓN UART

Escribir en la consola 

**sudo raspi-config**


![alt text](https://github.com/MariaFernandaG/raspberry/blob/main/im%C3%A1genes/uart1.PNG)

![alt text](https://github.com/MariaFernandaG/raspberry/blob/main/im%C3%A1genes/uart2.PNG)

![alt text](https://github.com/MariaFernandaG/raspberry/blob/main/im%C3%A1genes/uart3.PNG)

![alt text](https://github.com/MariaFernandaG/raspberry/blob/main/im%C3%A1genes/uart4.PNG)

![alt text](https://github.com/MariaFernandaG/raspberry/blob/main/im%C3%A1genes/uart5.PNG)


**sudo nano /boot/config.txt**

Agregar lo siguiente al final del texto:

- core_freq=250

- enable_uart=1

- dtoverlay = uart5

Para salir CTR+X, luego 'Y' para guardar y enter.

![alt text](https://github.com/MariaFernandaG/raspberry/blob/main/im%C3%A1genes/uart6.PNG "Ejemplo")

**sudo reboot**

[Link de referencia](https://www.sigmaelectronica.net/comunicacion-serial-raspberry-pi/)


## COMÁNDOS ÚTILES 

- sudo i2cdetect -y 1  (dirección de los sensores I2C)

- ls /dev/tty*  (ver la dirección para la comunicación serial)

- lsusb (ver disp. USB conectados)
