import socket
import json
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect(('192.168.0.100', 80))
message = json.dumps({'msg': sys.argv[1]})
sock.send(message.encode('utf-8'))
sock.shutdown(0)
sock.close()
