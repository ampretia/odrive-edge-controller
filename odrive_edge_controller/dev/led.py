from gpiozero import LED
from time import sleep

green_a = LED(5)
blue_a = LED(6)
blue_b = LED(13)
green_b = LED(19)
white = LED(26)
while True:
    white.on()
    sleep(1)
    white.off()
    sleep(1)