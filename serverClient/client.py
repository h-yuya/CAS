import socket

host = '192.168.0.42'
port = 12289

client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client.connect((host, port))

client.send('01WWRD00220,01,0001\r\n')
