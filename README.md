# SOS

Two people need to communicate with each other.  One is at one end of the room, the other at the other.  They communicate using Morse Code

Code for P3X talk - A Process fit for people, product and purpose.

Runs on a [NodeMCU](http://nodemcu.com/index_en.html)

[![Build Status](https://travis-ci.org/worldofchris/sos.svg?branch=master)](https://travis-ci.org/worldofchris)

## Dependencies

* Python 3

To get started, install the Python dependencies into a virtual environment with:

	make setup

## Configuring the beeping flashing thing

You will need to install the [OS-specific USB drivers](https://www.silabs.com/products/development-tools/software/usb-to-uart-bridge-vcp-drivers).

Then then flash the NodeMCU with the [latest MicroPython firmware](https://docs.micropython.org/en/latest/esp8266/esp8266/tutorial/intro.html#getting-the-firmware):

	make firmware

## Running the tests

	make test

## Deploying to a NodeMCU

Put the `SSID` and `password` for the WIFI you are using in a file called `wifi.txt` in the format:

	ssid,password

Then deploy with:

	make deploy 

## Usage

To send a message to be beeped and flashed by the device, connect to the same wifi network as the device and run:

	python send_message.py 'Your Message Here!'

There is a single reserved message `exit` which behaves as described in the *Hacking* section below.

## Hacking

To get to the REPL on the device:

	picocom -b 115200 /dev/tty.SLAB_USBtoUART

Then send the word `exit` to it over the wifi:

	python send_message.py exit
