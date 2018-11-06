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
        '.': '.−.−.−',
        ',': '--..--',
        "'": '.−−−−.',
        }

DURATION = .2
DIT = DURATION
DAH = DIT * 3
WORD_SPACE = (DIT * 7) * -1
CHAR_SPACE = (DIT * 3) * -1

def text_to_morse(text):
    """Translate text to morse"""
    morse = ''
    try:
        for i in text:
            if i == ' ':
                morse = morse[:-1]
                morse += CODE.get(i.upper())
            else:
                morse += CODE.get(i.upper())
                morse += ' '
        morse = morse[:-1]
    except TypeError as e:
        raise TranslationError from e
    return morse

def morse_to_signal(morse):
    """Translate morse to array of signal durations"""
    SIGNALS = {'.': DIT, '-': DAH, ' ': CHAR_SPACE, '/': WORD_SPACE}
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
        self.palette = {DIT: (255, 255, 255),
                        DAH: (255, 0,   0)}

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

class Beeper:
    """
    Piezo PWM Beeper
    """
    def __init__(self):
        self.pin = machine.Pin(2)
        self.pwm = machine.PWM(self.pin)
        self.freq = {DIT: 500, DAH: 250}
        self.duty = {DIT: 512, DAH: 256}
    def beep(self, signal):

        if signal == WORD_SPACE:
            time.sleep(DIT * 7)
        else:
            self.pwm.init(freq=500, duty=512)
            time.sleep(signal)
            self.pwm.deinit()

    def on(self, tone_index=DIT):
        self.pwm.init(freq=self.freq[tone_index], duty=self.duty[tone_index])

    def off(self):
        self.pwm.deinit()

class Sender:
    """
    Send messages via Beeps and Lights
    """
    def __init__(self, outputs=None):
        if outputs is None:
            outputs = [FlashLight(), Beeper()]
        self.outputs = outputs

    def send(self, message):
        morse_message = text_to_morse(message)
        signal = morse_to_signal(morse_message)
        for s in signal:
            print(s)
            if s in (WORD_SPACE, CHAR_SPACE):
                time.sleep(s * -1)
            else:
                for o in self.outputs:
                    o.on(s)
                    time.sleep(s)
                    o.off()
