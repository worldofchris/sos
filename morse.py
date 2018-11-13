"""
SOS
"""
import listner
import machine
import neopixel
import select
import socket
import sys
import time
import ujson

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

DURATION = .1
DIT = DURATION
DAH = DIT * 3
WORD_PAUSE = (DIT * 7) * -1
CHAR_PAUSE = (DIT * 3) * -1

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
    SIGNALS = {'.': DIT, '-': DAH, ' ': CHAR_PAUSE, '/': WORD_PAUSE}
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

class Beeper:
    """
    Piezo PWM Beeper
    """
    def __init__(self):
        self.pin = machine.Pin(2)
        self.pwm = machine.PWM(self.pin)
        self.freq = {DIT: 500, DAH: 500}
        self.duty = {DIT: 512, DAH: 512}
    def beep(self, signal):

        if signal == WORD_PAUSE:
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

class Listner:
    """
    Listen for messages to send
    """
    def __init__(self, wifi, name='morse', network=None, sender=None):
        self.name = name
        self.connection_status = False
        self.ssid = wifi[0]
        self.password = wifi[1]
        self.sock = None
        self.broadcast_ip_sock = None
        if network is not None:
            self.network = network
        else:
            self.network = network.WLAN(network.STA_IF)
        self.network.active(True)
        self.network.config(dhcp_hostname=self.name)
        self.network.connect(self.ssid, self.password)
        self.sender = sender

    def connect(self):
        """
        Connect to the WIFI network
        """
        DELAY = 2000
        print("connect")
        j = 0
        while not self.network.isconnected():
            j += 1
            if j >= DELAY:
                print("connecting...")
                j = 0
                # TODO Do some lights stuff

        self.connection_status = True
        self.sender.send("R")


    def connected(self):
        """Are we connected to the network?"""
        return self.connection_status

    def listen(self):
        """
        Listen for connections sending messages to send as morse
        """
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        sock = socket.socket()
        sock.bind(addr)
        sock.listen(1)

        print('listening on', addr)

        while self.connected():
            read_list, _, _ = select.select((sock,), (), (), 1)
            if read_list:
                for _ in read_list:
                    client, client_addr = sock.accept()
                    print('client connected from', client_addr)
                    body = ujson.loads(client.recv(1024))
                    try:
                        msg = body['msg']
                        print(msg)
                        if msg == 'exit':
                            sys.exit()
                        self.sender.send(msg)
                    except KeyError:
                        pass
                    client.send("ok")
                    client.close()
