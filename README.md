#SOS

Code for P3X talk - A Process fit for people, product and purpose.

Runs on a [nodemcu](http://nodemcu.com/index_en.html)

## Dependencies

[MicroPython](https://micropython.org/)

To get started, install the Python dependencies with:

	make develop

## Configuring the flasher

First erase the flash on the nodemcu:

	make erase

Then flash with the [MicroPython firmware](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#getting-the-firmware):

	make flash
	
## Running the tests

	make test

## Deploying to a nodemcu

	make deploy 

To get to the REPL on the device:

	picocom -b 115200 /dev/tty.SLAB_USBtoUART

