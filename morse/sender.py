from morse.translation import WORD_PAUSE, CHAR_PAUSE
from morse.translation import text_to_morse
from morse.translation import morse_to_signal
from morse.beeper import Beeper
from morse.flashlight import FlashLight
import time

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
        for i, s in enumerate(signal):
            print(morse_message[i], end='')
            if s in (WORD_PAUSE, CHAR_PAUSE):
                time.sleep(s * -1)
            else:
                for o in self.outputs:
                    o.on(s)
                    time.sleep(s)
                    o.off()
        print()