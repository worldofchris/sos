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
