import _thread
import time
import socket
import random
import sys

clients = []
bidsum = 0
base_bid = 0
best_bid = 0
best_client = 0
best_clientid = 0
INTERVALO = 5
med = 0

def client_handler(sock,client,address):
	size = 1024
	idcli = address[1]
	client.send("Your ID is: {}".format(idcli).encode())
	while True:
		try:
			data = client.recv(size).decode()
			data = int(data)
			print("Nova proposta > {}".format(data))
			global bidsum
			global best_clientid
			global clients
			global best_bid
			global best_client
			bidsum += data
			if data > best_bid:
				best_bid = data
				best_client = client 
				best_clientid = idcli
				print("BestBid {} - BestClient {}".format(best_bid, best_clientid))
			else:
				print("proposta foi menor que a melhor")         
		except socket.error as e:
			print("Erro > {}".format(e))
			client.close()
			clients.remove(client)
			return False

def create_bid(delay):
	while True:
		bid = random.randint(10,101)
		global basebid
		global best_bid
		global clients
		global best_clientid
		global best_client
		global bidsum
		basebid = bid
		best_bid = basebid
		best_client = 0
		bidsum = 0
		print("\nNova rodada")
		print("----------------------------------------")
		print("Proposta minima: {}".format(bid))
		for cli in clients:
			cli.send("NOVA RODADA".encode())
			time.sleep(.5)
			cli.send(str(bid).encode())
			time.sleep(.5)
		time.sleep(delay)
		
		if(len(clients) > 0):
			med = bidsum/len(clients)
		else:
			med = 0
			#
		if (best_bid > med*0.05 + med and best_client != 0):
			print("Cliente {} ganha com bid de {}".format(best_clientid,best_bid))
			for cli in clients:
				cli.send("Client {} ganha com bid de: {}".format(best_clientid, best_bid).encode())
				time.sleep(.5)
			best_client.send("Voce ganhou com a proposta de {}".format(best_bid).encode())
			time.sleep(.5)
		else:
			print("[!]Ninguem ganhou, nova rodada sera proposta!")
			for cli in clients:
				cli.send("Ninguem ganhou, nova rodada sera proposta!".encode())
		time.sleep(.5)	


# Create two threads as follows
try:
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	server_address = ('localhost', int(sys.argv[1]))
	sock.bind(server_address)
	sock.listen(5)
	print("Server escutando na porta {}".format(int(sys.argv[1])))
	_thread.start_new_thread( create_bid, (INTERVALO, ) )
	while True:
    # Wait for a connection
		client, address = sock.accept()
		clients.append(client)
		print("[!] Novo cliente -> {}".format(address[1]))
		_thread.start_new_thread( client_handler, (sock,client, address,) )

except :
   print ("Error")

while 1:
   pass