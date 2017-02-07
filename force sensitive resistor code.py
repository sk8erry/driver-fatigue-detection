#!/usr/bin/python
#Brian Kobylt and Ricky Yang
#Senior Project Driver Fatigue System (FSR and LED code)
 
import spidev
import time
import os
import RPi.GPIO as GPIO

# Open SPI bus
spi = spidev.SpiDev()
spi.open(0,0)
 
# Function to read SPI data from MCP3008 chip
# Channel must be an integer 0-7
def ReadChannel(channel):
  adc = spi.xfer2([1,(8+channel)<<4,0])
  data = ((adc[1]&3) << 8) + adc[2]
  return data
 
# Function to convert data to voltage level,
# rounded to specified number of decimal places.
def ConvertVolts(data,places):
  volts = (data * 3.3) / float(1023)
  volts = round(volts,places)
  return volts
  
# Function to calculate temperature from
# TMP36 data, rounded to specified
# number of decimal places.
def ConvertTemp(data,places):
 
  # ADC Value
  # (approx)  Temp  Volts
  #    0      -50    0.00
  #   78      -25    0.25
  #  155        0    0.50
  #  233       25    0.75
  #  310       50    1.00
  #  465      100    1.50
  #  775      200    2.50
  # 1023      280    3.30
 
  temp = ((data * 330)/float(1023))-50
  temp = round(temp,places)
  return temp

 # Define sensor channels
pressure_channel = 0

 # Define delay between readings
delay = .3

while True:
  
  # Read the light sensor data
  pressure_level = ReadChannel(pressure_channel)
  pressure_volts = ConvertVolts(pressure_level,2)


  # Print out results

  print ("--------------------------------------------")
  print("Pressure: {} ({}V)".format(pressure_level,pressure_volts))
  if pressure_level < 300:
    print ("HANDS OFF WHEEL!!!!!")
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.OUT)
    GPIO.output(16,0)
    GPIO.output(16,1)
    time.sleep(.3)
    GPIO.cleanup()

    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(15, GPIO.OUT)
    P = GPIO.PWM(15,100)
    P.start(30)
    time.sleep(.3)
    GPIO.cleanup()

##    GPIO.setmode(GPIO.BOARD)
##    GPIO.setup(22,GPIO.OUT)
##    GPIO.output(22,0)
##    GPIO.output(22,1)
##    time.sleep(.05)
##    GPIO.cleanup()
##
##    GPIO.setmode(GPIO.BOARD)
##    GPIO.setup(36,GPIO.OUT)
##    GPIO.output(36,0)
##    GPIO.output(36,1)
##    time.sleep(.05)
##    GPIO.cleanup()
##
##    GPIO.setmode(GPIO.BOARD)
##    GPIO.setup(11,GPIO.OUT)
##    GPIO.output(11,0)
##    GPIO.output(11,1)
##    time.sleep(.05)
##    GPIO.cleanup()
##
##    GPIO.setmode(GPIO.BOARD)
##    GPIO.setup(37,GPIO.OUT)
##    GPIO.output(37,0)
##    GPIO.output(37,1)
##    time.sleep(.05)
##    GPIO.cleanup()

##    GPIO.setmode(GPIO.BOARD)
##    GPIO.setup(31,GPIO.OUT)
##    GPIO.output(31,0)
##    GPIO.output(31,1)
##    time.sleep(.05)
##    GPIO.cleanup()
##
##    GPIO.setmode(GPIO.BOARD)
##    GPIO.setup(29,GPIO.OUT)
##    GPIO.output(29,0)
##    GPIO.output(29,1)
##    time.sleep(.05)
##    GPIO.cleanup()
else:
    GPIO.setmode(GPIO.BOARD)
    GPIO.setup(16,GPIO.OUT)
    GPIO.output(16,0)
    time.sleep(1)

    # Wait before repeating loop




  
