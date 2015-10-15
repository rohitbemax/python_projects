import socket
import binascii
import time

HOST = '127.0.0.1'    # The remote host
PORT = 5555           # The same port as used by the server


#Slot 2, we disconnect after the timeout and then send the data again and wait for the data the come from the server
ts = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
ts.connect((HOST, PORT))
ts.send(bytearray([0x00, 0x01, 0x02]))
data = ts.recv(1024)
hex = str(binascii.hexlify(data), 'ascii')
formatted_hex = ', '.join(hex[i:i+2] for i in range(0, len(hex), 2))
print("Data received", formatted_hex)
