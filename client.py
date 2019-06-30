import socket
import sys
import random

sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
if len(sys.argv) < 3:
	sys.exit("[X] IP or port not provided correctly! - Usage: python3 <script.py> <host> <port>");
server_address = (str(sys.argv[1]), int(sys.argv[2]))
sock.connect(server_address)

MAXBID = 300

while True:
	try:
		msg = sock.recv(1024).decode()
		if (msg == "NOVA RODADA"):
			print("\nNova rodada!")
			print("----------------------")
			basebid = sock.recv(1024).decode()
			mybid = random.randint(int(basebid),MAXBID);
			print("Enviando proposta de {}".format(mybid))
			sock.send(str(mybid).encode())
		else:
			print(msg)
	except socket.error as e:
		print("err - {}".format(e))