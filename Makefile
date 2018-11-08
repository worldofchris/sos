SRC := morse.py main.py wifi.txt
PORT := /dev/tty.SLAB_USBtoUART
FIRMARE := esp8266-20180511-v1.9.4.bin
PYTHON := python3
ACTIVATE := venv/bin/activate

.PHONY: virtualenv develop deploy torch erase firmware

test: **/*.py
	nosetests

deploy: torch
	source $(ACTIVATE) && \
		for FILE in $(SRC) ; do \
			ampy --port $(PORT) put $$FILE ; \
		done

virtualenv:
	$(PYTHON) -m venv venv

develop: virtualenv
	source $(ACTIVATE) && \
		pip install -r requirements.txt

torch: erase firmware

erase:
	source $(ACTIVATE) && \
		esptool.py -p $(PORT) erase_flash

firmware:
	source $(ACTIVATE) && \
		esptool.py --port $(PORT) --baud 460800 write_flash --flash_size=detect 0 $(FIRMARE)
