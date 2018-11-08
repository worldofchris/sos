#SOS

Two people need to communicate with each other.  One is at one end of the room, the other at the other.  They communicate using Morse Code

Code for P3X talk - A Process fit for people, product and purpose.

Runs on a [nodemcu](http://nodemcu.com/index_en.html)

## Dependencies

[MicroPython](https://micropython.org/)

To get started, install the Python dependencies with:

	make develop

## Configuring the beeping flashing thing

First erase the flash on the nodemcu:

	make erase

Then flash with the [MicroPython firmware](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#getting-the-firmware):

	make flash
	
## Running the tests

	make test

## Deploying to a nodemcu

Put the `SSID` and `password` for the WIFI you are using in a file called `wifi.txt` in the format:

	ssid,password

Then deploy with:

	make deploy 

## Usage

To send a message to be beeped and flashed by the device, connect to the same wifi network as the device and run:

	python send_message.py Your Message Here!

There is a single reserved message `exit` which behaves as described in the *Hacking* section below.

## Hacking

To get to the REPL on the device:

	picocom -b 115200 /dev/tty.SLAB_USBtoUART

Then send the word `exit` to it over the wifi:

	python send_message.py exit
