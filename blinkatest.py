#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu May 28 21:12:12 2020

@author: pi
"""
import time
import RPi.GPIO as GPIO
import board
import busio
import adafruit_adxl34x
import numpy as np
import matplotlib.pyplot as plt

GPIO.setmode(GPIO.BCM)
GPIO.setup(17, GPIO.OUT)
GPIO.setup(27, GPIO.OUT)

#Inicjalizacja Akcelerometrow
i2c = busio.I2C(board.SCL, board.SDA)
print("I2C ok!")

accelerometr0 = adafruit_adxl34x.ADXL343(i2c, address=0x53)
accelerometr1 = adafruit_adxl34x.ADXL343(i2c, address=0x1D)

print("done!")

#Parametry
pitch0 = roll0 = pitch1 = roll1 = 0
alpha = 0.6
fXg0 = fYg0 = fZg0 = fXg1 = fYg1 = fZg1 = 0

plotData_Xg = []
plotData_Yg = []
plotData_Zg = []
plotData_fXg = []
plotData_fYg = []
plotData_fZg = []

plotData_Xg.append(0)
plotData_Yg.append(0)
plotData_Zg.append(0)
plotData_fXg.append(0)
plotData_fYg.append(0)
plotData_fZg.append(0)

i = 0
while i<150:
    #Accelerations
    Xg0, Yg0, Zg0 = accelerometr0.acceleration
    Xg1, Yg1, Zg1 = accelerometr1.acceleration

    #Low Pass Filter
    fXg0 = Xg0 * alpha + (fXg0 * (1.0 - alpha));
    fYg0 = Yg0 * alpha + (fYg0 * (1.0 - alpha));
    fZg0 = Zg0 * alpha + (fZg0 * (1.0 - alpha));
    fXg1 = Xg1 * alpha + (fXg1 * (1.0 - alpha));
    fYg1 = Yg1 * alpha + (fYg1 * (1.0 - alpha));
    fZg1 = Zg1 * alpha + (fZg1 * (1.0 - alpha));

    plotData_Xg.append(Xg0)
    plotData_Yg.append(Yg0)
    plotData_Zg.append(Zg0)
    plotData_fXg.append(fXg0)
    plotData_fYg.append(fYg0)
    plotData_fZg.append(fZg0)

    #plotData.append([Xg0, Yg0, Zg0, fXg0, fYg0, fZg0])
    #print('fXg0: ',"%.5f" %  fXg0, ', fYg0: ',"%.5f" %  fYg0, ', fZg0: ',"%.5f" %  fZg0, ' || ', 'fXg1: ',"%.5f" %  fXg1, ', fYg1: ',"%.5f" %  fYg1, ', fZg1: ',"%.5f" %  fZg1)

    #Roll & Pitch Equations
    roll0  = (np.arctan2(-fYg0, fZg0)*180.0)/np.pi;
    pitch0 = (np.arctan2(fXg0, np.sqrt(fYg0*fYg0 + fZg0*fZg0))*180.0)/np.pi;

    roll1  = (np.arctan2(-fYg1, fZg1)*180.0)/np.pi;
    pitch1 = (np.arctan2(fXg1, np.sqrt(fYg1*fYg1 + fZg1*fZg1))*180.0)/np.pi;

    #print((roll0, pitch0, roll1, pitch1))
    rolled = roll1 - roll0
    pitched = pitch0

    targetDegree = 45
    error = 2

    if rolled >= (targetDegree - error) and rolled <= (targetDegree + error):
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.LOW)
    elif rolled > (targetDegree + error):
        GPIO.output(17, GPIO.HIGH)
        GPIO.output(27, GPIO.LOW)
    elif rolled < (targetDegree - error):
        GPIO.output(17, GPIO.LOW)
        GPIO.output(27, GPIO.HIGH)

    print((rolled, roll0, roll1, pitched))
    time.sleep(0.1)
    i = i+1
    print('i = ', i)
    #c, addr = tcp.accept()
    #print('Get connection from: ', addr)
    #c.send(bytearray(b'Testowa ramka TCP!'))

GPIO.cleanup()
plt.plot(plotData_Xg, 'red', label = 'Xg')
plt.plot(plotData_fXg, 'orchid', label = 'fXg')
plt.plot(plotData_Yg, 'darkorange', label = 'Yg')
plt.plot(plotData_fYg, 'gold', label = 'fYg')
plt.plot(plotData_Zg, 'forestgreen', label = 'Zg')
plt.plot(plotData_fZg, 'lime', label = 'fZg')
plt.legend(loc='center left', bbox_to_anchor=(1,0.5))
plt.show()