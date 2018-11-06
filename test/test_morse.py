"""
SOS Tests
"""
import time
import unittest
from unittest.mock import patch, call, Mock
from morse import text_to_morse, morse_to_signal, DIT, DAH, FlashLight, flash_message, WORD_SPACE, TranslationError, Beeper

class TestSOS(unittest.TestCase):
    """Test ways of sending SOS"""

    def setUp(self):
        self.text_message = "SOS"
        self.morse_message = "... --- ..."

    def test_translate_to_morse(self):
        """Translate ASCII text to morse"""
        message = text_to_morse(self.text_message)
        assert message == self.morse_message, message

    def test_translate_morse_to_signal(self):
        """Translate morse representation to DITs and DAHs"""
        signal = morse_to_signal(self.morse_message)
        assert signal == [DIT, DIT, DIT, None,
                          DAH, DAH, DAH, None,
                          DIT, DIT, DIT], signal

    @patch('neopixel.NeoPixel')
    @patch('time.sleep', return_value=None)
    def test_flash_light(self, NeoPixel, patched_time_sleep):
        """Flash the light"""
        fl = FlashLight()
        fl.flash(DIT)
        assert fl.neo_pixel.__setitem__.call_count == 2, fl.neo_pixel.__setitem__.call_count
        assert time.sleep.call_count == 1
        time.sleep.assert_called_with(DIT)
        assert fl.neo_pixel.write.call_count == 2, fl.neo_pixel.write.call_count # ON / OFF

    def test_flash_message(self):
        """Send a message"""
        fl = Mock()
        calls = [call(DIT), call(DIT), call(DIT),
                 call(None),
                 call(DAH), call(DAH), call(DAH),
                 call(None),
                 call(DIT), call(DIT), call(DIT)]
        flash_message(fl, self.text_message)
        fl.flash.assert_has_calls(calls)

    def test_long_message(self):
        """Send a long message"""
        long_msg = "The quick brown fox jumped over the lazy dog"
        fl = Mock()
        flash_message(fl, long_msg)
        assert fl.flash.call_count == 156

    @patch('neopixel.NeoPixel')
    @patch('time.sleep', return_value=None)    
    def test_flash_space(self, NeoPixel, patched_time_sleep):
        """Flash a message with spaces in it.  Light should not go on"""
        fl = FlashLight()
        fl.flash(WORD_SPACE)
        assert fl.neo_pixel.__setitem__.call_count == 0, fl.neo_pixel.__setitem__.call_count
        assert time.sleep.call_count == 1
        time.sleep.assert_called_with(DIT * 7)
        assert fl.neo_pixel.write.call_count == 0, fl.neo_pixel.write.call_count # ON / OFF

    def test_message_with_punctuation(self):
        """Flash a message with punctuation"""
        punc_msg = "When you're near me, darling can't you hear me S.O.S."
        fl = Mock()
        flash_message(fl, punc_msg)
        assert fl.flash.call_count == 192

    def test_fail_gracefully(self):
        """Fail gracefully if cannoy translate message to morse"""
        fail_msg = "!LOLS^^^This wont work @ all :-)"
        fl = Mock()
        with self.assertRaises(TranslationError):
            flash_message(fl, fail_msg)

    @patch('time.sleep', return_value=None)    
    @patch('machine.PWM')
    @patch('machine.Pin')
    def test_beep_message(self, pin, pwm, patched_time_sleep):
        """Send a message as a buzz on the buzzer"""
        beeper = Beeper()
        beeper.beep(DIT)
        pin.assert_called_with(2)
        pwm.assert_called_with(beeper.pin)
        assert beeper.pwm.init.call_count == 1, beeper.pwm.init.call_count
        assert time.sleep.call_count == 1
        time.sleep.assert_called_with(DIT)
        assert beeper.pwm.deinit.call_count == 1, beeper.pwm.deinit.call_count
