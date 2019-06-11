import Adafruit_CharLCD as LCD
import time

lcd_rs        = 26
lcd_en        = 19
lcd_d4        = 13
lcd_d5        = 6
lcd_d6        = 5
lcd_d7        = 11
lcd_backlight = 4
lcd_columns = 16
lcd_rows = 2

lcd_armed_default = "Armed"
lcd_breach_default = "BREACH!"

#init LCD with above options
lcd = LCD.Adafruit_CharLCD(lcd_rs, lcd_en, lcd_d4, lcd_d5, lcd_d6, lcd_d7,
                           lcd_columns, lcd_rows, lcd_backlight)


def show_message(msg, clear=None, timeout=5.0):
    lcd.clear()
    lcd.message(msg)
    if clear is not None:
        time.sleep(float(timeout))
        lcd.clear()
        lcd.message(lcd_armed_default)
        
