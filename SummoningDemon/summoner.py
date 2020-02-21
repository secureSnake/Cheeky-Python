#!/usr/bin/python3
import socket      
import argparse     
import os           
import threading       
import queue           
import demonUtil
import sys

q = queue.Queue()
demonUtil.DemonThreads = []
parser = argparse.ArgumentParser(description="Summon a horde of demons. Usage python3 summoner.py <host> <port> \n.", add_help=True)
parser.add_argument('host', type=str, help='IP address to listen on')
parser.add_argument('port', type=int, help='Port to listen on')

def listen(lhost, lport, q):
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    #server.settimeout(60)
    server_address = (lhost, lport)
    server.bind(server_address)
    server.listen(20) #change this if more connections desired

    print ("[+] Summoning demons on " + lhost + ":" + str(lport) + "\n")

    #start summoner terminal
    Summoner = demonUtil.SummonerConsole(q)
    Summoner.start()

    #store any new connections

    while True:
        (clientsock, client_address) = server.accept()
        print("New demon reporting in!")
        newthread = demonUtil.Demon(clientsock, client_address, q)
        demonUtil.DemonThreads.append(newthread)



def main():
    try:
        args = parser.parse_args()
        lhost = args.host
        lport = args.port    
        listen(lhost, lport, q)
    except Exception as ex:
        print("\n[-] Something went wrong...details: " + str(ex) + "\n")
        #parser.print_help()
if __name__ == '__main__':
    main()
