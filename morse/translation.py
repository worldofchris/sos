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
        '.': '.-.-.-',
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
