import gpiozero
from helpers import door_switch, db, send_mail, buzzer, lcd_display
#from helpers.lcd_display import *

#door_switch functions
button = gpiozero.Button(18)
button.when_pressed = door_switch.armed
button.when_released = door_switch.breach






