SRC := morse.py main.py wifi.txt
PORT := /dev/tty.SLAB_USBtoUART
PYTHON := python3
WORK_DIR := work
FIRMWARE_URL := http://micropython.org/resources/firmware/esp8266-20180511-v1.9.4.bin
FIRMWARE := $(WORK_DIR)/firmware.bin
ACTIVATE := $(WORK_DIR)/venv/bin/activate

.PHONY: deploy erase_flash firmware get_firmware setup test virtualenv

test:
	source $(ACTIVATE) && \
		nosetests

virtualenv:
	python3 -mvenv sos_env
	pwd && . $(ACTIVATE) && \
		pip install -r requirements.txt

get_firmware:
	test -d deps || mkdir deps
	curl $(FIRMWARE_URL) -o $(FIRMWARE)

setup: virtualenv get_firmware

deploy: erase_flash firmware
	source $(ACTIVATE) && \
		for FILE in $(SRC) ; do \
			ampy --port $(PORT) put $$FILE ; \
		done

erase_flash:
	source $(ACTIVATE) && \
		esptool.py -p $(PORT) erase_flash

firmware: erase_flash
	source $(ACTIVATE) && \
		esptool.py --port $(PORT) --baud 460800 write_flash --flash_size=detect 0 $(FIRMWARE)
