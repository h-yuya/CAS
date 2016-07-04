import RPi.GPIO as gpio
import time
import wiringpi2 as wiringpi

delay = 0.2
outpin = 17

gpio.setmode(gpio.BCM)
gpio.setup(outpin, gpio.OUT)

wiringpi.wiringPiSetupGpio()
wiringpi.softToneCreate(outpin)


wiringpi.softToneWrite(outpin, 523)
time.sleep(0.2)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 523)
time.sleep(0.2)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 523)
time.sleep(0.2)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 523)
time.sleep(0.6)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 415)
time.sleep(0.6)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 466)
time.sleep(0.6)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 523)
time.sleep(0.4)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 466)
time.sleep(0.2)
wiringpi.softToneWrite(outpin, 0)
time.sleep(0.01)
wiringpi.softToneWrite(outpin, 523)
time.sleep(0.7)
wiringpi.softToneWrite(outpin, 0)

gpio.cleanup()
