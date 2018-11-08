"""
SOS Tests
"""
import time
import unittest
from unittest.mock import patch, call, Mock
from morse import text_to_morse, \
                  morse_to_signal, DIT, DAH, FlashLight, \
                  flash_message, CHAR_SPACE, WORD_SPACE, \
                  TranslationError, Beeper, Sender, \
                  Listner

class TestSOS(unittest.TestCase):
    """Test ways of sending SOS"""

    def setUp(self):
        self.text_message = "SOS"
        self.morse_message = "... --- ..."
        self.long_msg = "The quick brown fox jumped over the lazy dog"

    def test_translate_to_morse(self):
        """Translate ASCII text to morse"""

        message = text_to_morse(self.text_message)
        assert message == self.morse_message, message

    def test_translate_long_to_morse(self):
        """Are we dealing with word spaces correctly?"""
        message = text_to_morse(self.long_msg)
        assert message == '- .... ./--.- ..- .. -.-. -.-/-... .-. --- .-- -./..-. --- -..-/.--- ..- -- .--. . -../--- ...- . .-./- .... ./.-.. .- --.. -.--/-.. --- --.', message

    def test_translate_morse_to_signal(self):
        """Translate morse representation to DITs and DAHs"""
        signal = morse_to_signal(self.morse_message)
        assert signal == [DIT, DIT, DIT, CHAR_SPACE,
                          DAH, DAH, DAH, CHAR_SPACE,
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
                 call(CHAR_SPACE),
                 call(DAH), call(DAH), call(DAH),
                 call(CHAR_SPACE),
                 call(DIT), call(DIT), call(DIT)]
        flash_message(fl, self.text_message)
        fl.flash.assert_has_calls(calls) # Think we are not respecting order here

    def test_long_message(self):
        """Send a long message"""
        fl = Mock()
        flash_message(fl, self.long_msg)
        # calls = [call(DIT), call(8)]
        # fl.flash.assert_has_calls(calls)
        assert fl.flash.call_count == 140, fl.flash.call_count

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
        assert fl.flash.call_count == 174, fl.flash.call_count

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

    @patch('time.sleep', return_value=None)
    def test_beep_and_flash_together(self, patched_time_sleep):
        """Beep and Flash at the same time"""
        beeper = Mock()
        fl = Mock()

        sender = Sender([beeper, fl])
        sender.send(self.text_message)
        assert beeper.on.call_count == 9, beeper.on.call_count
        assert beeper.off.call_count == 9, beeper.off.call_count
        assert fl.on.call_count == 9, fl.on.call_count
        assert fl.off.call_count == 9, fl.off.call_count

    @patch('neopixel.NeoPixel')
    def test_flash_on(self, NeoPixel):
        """Turn light on"""
        fl = FlashLight()
        fl.on()
        assert fl.neo_pixel.__setitem__.call_count == 1, fl.neo_pixel.__setitem__.call_count
        assert fl.neo_pixel.write.call_count == 1, fl.neo_pixel.write.call_count

    @patch('neopixel.NeoPixel')
    def test_flash_off(self, NeoPixel):
        """Turn light off"""
        fl = FlashLight()
        fl.off()
        assert fl.neo_pixel.__setitem__.call_count == 1, fl.neo_pixel.__setitem__.call_count
        fl.neo_pixel.__setitem__.assert_called_with(0, (0, 0, 0))
        assert fl.neo_pixel.write.call_count == 1, fl.neo_pixel.write.call_count

    @patch('machine.PWM')
    @patch('machine.Pin')
    def test_beep_on(self, pin, pwm):
        """Beep on"""
        beeper = Beeper()
        beeper.on()
        pin.assert_called_with(2)
        pwm.assert_called_with(beeper.pin)
        assert beeper.pwm.init.call_count == 1, beeper.pwm.init.call_count

    @patch('machine.PWM')
    @patch('machine.Pin')
    def test_beep_off(self, pin, pwm):
        """Beep off"""
        beeper = Beeper()
        beeper.off()
        pin.assert_called_with(2)
        pwm.assert_called_with(beeper.pin)
        assert beeper.pwm.deinit.call_count == 1, beeper.pwm.deinit.call_count

    @patch('neopixel.NeoPixel')
    def test_dah_colour(self, NeoPixel):
        """Make dah a different colour so it is easier to distinguish"""
        fl = FlashLight()
        fl.on(DAH)
        fl.neo_pixel.__setitem__.assert_called_with(0, fl.palette[DAH])

    @patch('machine.PWM')
    @patch('machine.Pin')
    def test_dah_tine(self, pin, pwn):
        """Make dah a different tone so it easier to distinguish"""
        beeper = Beeper()
        beeper.on(DAH)
        beeper.pwm.init.assert_called_with(freq=beeper.freq[DAH], duty=beeper.duty[DAH])

    # @patch('socket.socket')
    # @patch('imp.node.select')
    # def test_tcp_listen(self, select, socket):
    #     """
    #     It listens for incoming messages to send
    #     """
    #     mock_socket, mock_incoming_socket = self.mock_socket(socket, select, {'msg': 'Old Mr B, Riddle Me Re'})
    #     self.mocked_network_node.tcp_listen()
    #     assert mock_socket.accept.call_count == 1
    #     mock_incoming_socket.send.assert_called_with('ok')
    #     assert mock_incoming_socket.close.call_count == 1
    #     assert listener.sender.send.call_count == 1


    @patch('socket.socket')
    def test_connect_to_network(self, socket):
        """
        It searches for a network to connect to
        """
        WIFI = ('ssid', 'password')
        network = Mock()

        network.connect = Mock()
        network.isconnected = Mock()
        connection_status = [False, False, True]
        network.isconnected.side_effect = connection_status
        sender = Mock()
        listner = Listner(WIFI, 'morse', network, sender)
        listner.connect()
        listner.network.active.assert_called_with(True)
        assert listner.network.connect.call_count == 1
        assert listner.network.isconnected.call_count == len(connection_status), listner.network.isconnected.call_count
        assert listner.sender.send.call_count == 1
