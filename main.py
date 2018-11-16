"""
SOS
"""
import network
from morse import Listener, Sender

net = network.WLAN(network.STA_IF)
wifi_creds = open('wifi.txt')
wifi = wifi_creds.read().rstrip().split(',')
wifi_creds.close()

s = Sender()
l = Listener(wifi, "morse", net, s)
l.connect()
l.listen()
