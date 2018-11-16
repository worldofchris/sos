import select
import socket
import sys
import ujson

class Listener:
    """
    Listen for messages to send
    """
    def __init__(self, wifi, name='morse', network=None, sender=None):
        self.name = name
        self.connection_status = False
        self.ssid = wifi[0]
        self.password = wifi[1]
        self.sock = None
        self.broadcast_ip_sock = None
        if network is not None:
            self.network = network
        else:
            self.network = network.WLAN(network.STA_IF)
        self.network.active(True)
        self.network.config(dhcp_hostname=self.name)
        self.network.connect(self.ssid, self.password)
        self.sender = sender

    def connect(self):
        """
        Connect to the WIFI network
        """
        DELAY = 2000
        print("connect")
        j = 0
        while not self.network.isconnected():
            j += 1
            if j >= DELAY:
                print("connecting...")
                j = 0
                # TODO Do some lights stuff

        self.connection_status = True
        self.sender.send("R")


    def connected(self):
        """Are we connected to the network?"""
        return self.connection_status

    def listen(self):
        """
        Listen for connections sending messages to send as morse
        """
        addr = socket.getaddrinfo('0.0.0.0', 80)[0][-1]

        sock = socket.socket()
        sock.bind(addr)
        sock.listen(1)

        print('listening on', addr)

        while self.connected():
            read_list, _, _ = select.select((sock,), (), (), 1)
            if read_list:
                for _ in read_list:
                    client, client_addr = sock.accept()
                    print('client connected from', client_addr)
                    body = ujson.loads(client.recv(1024))
                    try:
                        msg = body['msg']
                        print(msg)
                        if msg == 'exit':
                            sys.exit()
                        self.sender.send(msg)
                    except KeyError:
                        pass
                    client.send("ok")
                    client.close()
