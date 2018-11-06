SRC := morse.py main.py
PORT := /dev/tty.SLAB_USBtoUART
FIRMARE := esp8266-20180511-v1.9.4.bin

test: **/*.py
	nosetests

deploy: $(SRC) wifi.txt
	for FILE in $(SRC) ; do \
		ampy --port $(PORT) put $$FILE ; \
	done

develop: requirements.txt
	pip install -r requirements.txt

erase:
	esptool.py -p $(PORT) erase_flash

firmware:
	esptool.py --port $(PORT) --baud 460800 write_flash --flash_size=detect 0 $(FIRMARE)
