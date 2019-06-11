import time
from helpers.lcd_display import *
from helpers.buzzer import *

def armed():
    print('Door switch armed')
    show_message(lcd_armed_default)
    if bz.is_active:
        bz.stop()
    bz.play(tone_armed)
    time.sleep(0.5)
    bz.stop()

def breach():
    print('Door breached!')
    show_message(lcd_breach_default)
    bz.play(tone_breach)
