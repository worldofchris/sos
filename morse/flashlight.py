from morse.translation import DIT
from morse.translation import DAH, DIT, WORD_PAUSE, CHAR_PAUSE
from morse.translation import text_to_morse
from morse.translation import morse_to_signal
import neopixel
import machine
import time

class FlashLight:
    """
    Neopixel Flash Light
    """
    def __init__(self):
        self.neo_pixel = neopixel.NeoPixel(machine.Pin(0), 1)
        self.palette = {DIT: (255, 255, 255),
                        DAH: (255, 0,   0)}

    def flash(self, signal):
        """
        Flash the light
        """
        if signal == WORD_PAUSE:
            time.sleep(DIT * 7)
        else:
            self.neo_pixel[0] = (255, 255, 255)
            self.neo_pixel.write()
            time.sleep(signal)
            self.neo_pixel[0] = (0, 0, 0)
            self.neo_pixel.write()

    def on(self, color_index=DIT):
        self.neo_pixel[0] = (self.palette[color_index])
        self.neo_pixel.write()

    def off(self):
        self.neo_pixel[0] = (0, 0, 0)
        self.neo_pixel.write()

def flash_message(flashlight, text_message):
    morse_message = text_to_morse(text_message)
    signal_message = morse_to_signal(morse_message)
    for signal in signal_message:
        flashlight.flash(signal)
