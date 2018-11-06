"""
SOS
"""
import time
import neopixel
import machine

class TranslationError(Exception):
    """We could not translate to morse"""
    pass

CODE = {'A': '.-',     'B': '-...',   'C': '-.-.', 
        'D': '-..',    'E': '.',      'F': '..-.',
        'G': '--.',    'H': '....',   'I': '..',
        'J': '.---',   'K': '-.-',    'L': '.-..',
        'M': '--',     'N': '-.',     'O': '---',
        'P': '.--.',   'Q': '--.-',   'R': '.-.',
        'S': '...',    'T': '-',      'U': '..-',
        'V': '...-',   'W': '.--',    'X': '-..-',
        'Y': '-.--',   'Z': '--..',

        '0': '-----',  '1': '.----',  '2': '..---',
        '3': '...--',  '4': '....-',  '5': '.....',
        '6': '-....',  '7': '--...',  '8': '---..',
        '9': '----.',

        ' ': '/',
        '.': '·−·−·−',
        ',': '−−··−−',
        "'": '·−−−−·',
        }

WORD_SPACE = -1
DURATION = 1
DIT = DURATION
DAH = DIT * 3

def text_to_morse(text):
    """Translate text to morse"""
    try:
        return ' '.join(CODE.get(i.upper()) for i in text)
    except TypeError as e:
        raise TranslationError from e

def morse_to_signal(morse):
    """Translate morse to array of signal durations"""
    SIGNALS = {'.': DIT, '-': DAH, ' ': None, '/': WORD_SPACE}
    result = []
    for i in morse:
        result.append(SIGNALS.get(i))
    return result

class FlashLight:
    """
    Neopixel Flash Light
    """
    def __init__(self):
        self.neo_pixel = neopixel.NeoPixel(machine.Pin(0), 1)

    def flash(self, signal):
        """
        Flash the light
        """
        if signal == WORD_SPACE:
            time.sleep(DIT * 7)
        else:
            self.neo_pixel[0] = (255, 255, 255)
            self.neo_pixel.write()
            time.sleep(signal)
            self.neo_pixel[0] = (0, 0, 0)
            self.neo_pixel.write()

def flash_message(flashlight, text_message):
    morse_message = text_to_morse(text_message)
    signal_message = morse_to_signal(morse_message)
    for signal in signal_message:
        flashlight.flash(signal)
