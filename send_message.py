import socket
import json
import sys

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sock.connect((sys.argv[1], 80))
message = json.dumps({'msg': sys.argv[2]})
sock.send(message.encode('utf-8'))
sock.shutdown(0)
sock.close()
