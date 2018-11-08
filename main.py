"""
SOS
"""
import network
from morse import Listner, Sender

net = network.WLAN(network.STA_IF)
wifi_creds = open('wifi.txt')
wifi = wifi_creds.read().rstrip().split(',')
wifi_creds.close()

s = Sender()
l = Listner(wifi, "morse", net, s)
l.connect()
l.listen()