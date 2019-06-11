import gpiozero
from gpiozero.tones import Tone

tone_breach = Tone(500.0)
tone_armed = Tone(60.0)

bz = gpiozero.TonalBuzzer(23)

